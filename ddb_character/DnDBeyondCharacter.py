import os
import requests
import openai


class DnDBeyondCharacter:
    def __init__(self, character_id):
        self.base_url = (
            "https://character-service.dndbeyond.com/character/v3/character/"
        )
        self.character_id = character_id
        self.ddb_data = None
        self.name = None

        openai.api_key = os.environ["OPENAI_API_KEY"]

    def __str__(self):
        appearance_data = self.get_appearance_data()
        character_data = self.get_character_data()

        return f"{self.name}\n{appearance_data['gender']} {appearance_data['race']}\n{character_data['class_levels']}"

    def get_ddb_data(self):
        url = f"{self.base_url}{self.character_id}"

        response = requests.get(url)

        if response.status_code == 200:
            self.ddb_data = response.json()
            self.name = self.ddb_data["data"].get("name", "Unknown")
            print(f"Received data for {self.name}")
            return self.ddb_data
        else:
            raise Exception(
                f"Error: {response.status_code} - Could not download character data"
            )

    def get_openai_text(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        return response.choices[0].text.strip()

    def get_appearance_data(self):
        if not self.ddb_data:
            self.get_ddb_data()

        appearance_data = {
            "gender": self.ddb_data["data"].get("gender", "Unknown"),
            "age": self.ddb_data["data"].get("age", "Unknown"),
            "eyes": self.ddb_data["data"].get("eyes", "Unknown"),
            "hair": self.ddb_data["data"].get("hair", "Unknown"),
            "height": self.ddb_data["data"].get("height", "Unknown"),
            "weight": self.ddb_data["data"].get("weight", "Unknown"),
            "skin": self.ddb_data["data"].get("skin", "Unknown"),
            "race": self.ddb_data["data"]["race"].get("fullName", "Unknown"),
            "appearance": self.ddb_data["data"]["traits"].get("appearance", "Unknown"),
            "personalPossessions": self.ddb_data["data"]["notes"].get(
                "personalPossessions", "Unknown"
            ),
        }

        return appearance_data

    def get_character_backstory(self):
        if not self.ddb_data:
            self.get_ddb_data()

        return self.ddb_data["data"]["notes"].get("backstory", "Unknown")

    def get_character_data(self):
        if not self.ddb_data:
            self.get_ddb_data()

        character_data = {
            "background": self.ddb_data["data"]["background"].get("name", "Unknown"),
            "class_levels": ", ".join(
                [
                    f"{c['definition']['name']} {c['level']}"
                    for c in self.ddb_data["data"]["classes"]
                ]
            ),
            "faith": self.ddb_data["data"].get("faith", "Unknown"),
            "personalityTraits": self.ddb_data["data"]["traits"].get(
                "personalityTraits", "Unknown"
            ),
            "ideals": self.ddb_data["data"]["traits"].get("ideals", "Unknown"),
            "bonds": self.ddb_data["data"]["traits"].get("bonds", "Unknown"),
            "flaws": self.ddb_data["data"]["traits"].get("flaws", "Unknown"),
            "allies": self.ddb_data["data"]["notes"].get("allies", "Unknown"),
            "organizations": self.ddb_data["data"]["notes"].get(
                "organizations", "Unknown"
            ),
            "enemies": self.ddb_data["data"]["notes"].get("enemies", "Unknown"),
            "otherHoldings": self.ddb_data["data"]["notes"].get(
                "otherHoldings", "Unknown"
            ),
        }

        return character_data

    def generate_description(self):
        appearance_data = self.get_appearance_data()
        character_data = self.get_appearance_data()

        prompt = ". ".join(
            [
                f"Describe a DnD character with the following physical characteristing: {appearance_data}",
                f"Consider also this information for context: {character_data}",
            ]
        )

        text = self.get_openai_text(prompt)
        return text

    def generate_backstory(self):
        appearance_data = self.get_appearance_data()
        character_data = self.get_character_data()
        existing_backstory = self.get_character_backstory()

        prompt = ". ".join(
            [
                f"Create a backstory for a DnD character named {self.name}, who is a {appearance_data['gender']} {appearance_data['race']}",
                f"The backstory should fit with the following information: {character_data}",
                f"The backstory should use the following text for inspiration, if not 'Unknown': {existing_backstory}",
            ]
        )

        text = self.get_openai_text(prompt)
        return text

    def print_appearance_data(self):
        appearance_data = self.get_appearance_data()
        print("Character Description Data:")
        for key, value in appearance_data.items():
            print(f"{key.capitalize()}: {value}")


# Usage example
if __name__ == "__main__":
    character_id = 44962573
    character = DnDBeyondCharacter(character_id)
    print(character)
    # print(character.get_appearance_data())
    description = character.generate_description()
    print(description)
    backstory = character.generate_backstory()
    print(backstory)

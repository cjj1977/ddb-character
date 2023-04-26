import unittest
from unittest.mock import patch
from ddb_character import DnDBeyondCharacter


class TestDnDBeyondCharacter(unittest.TestCase):
    def setUp(self):
        self.character_id = 44962573
        self.downloader = DnDBeyondCharacter(self.character_id)

    @patch("requests.get")
    def test_download_character_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": self.character_id}

        character_data = self.downloader.download_character()

        self.assertIsNotNone(character_data)
        self.assertEqual(character_data["id"], self.character_id)
        mock_get.assert_called_with(
            f"https://character-service.dndbeyond.com/character/v3/character/{self.character_id}"
        )

    @patch("requests.get")
    def test_download_character_failure(self, mock_get):
        mock_get.return_value.status_code = 404

        with self.assertRaises(Exception) as context:
            self.downloader.download_character()

        self.assertEqual(
            str(context.exception), f"Error: 404 - Could not download character data"
        )


if __name__ == "__main__":
    unittest.main()

from setuptools import setup, find_packages

setup(
    name="ddb_character",
    version="0.1.0",
    packages=find_packages(include=["ddb_character"]),
    install_requires=[
        "requests",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "ddb_character=ddb_character:main",
        ],
    },
)

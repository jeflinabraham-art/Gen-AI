import json
from pathlib import Path


# Reads a text file.
def read_text(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")




# Writes content to a text file.
def write_text(file_path: str, content: str):

    # If file doesn't exist, write_text() normally creates it, provided its parent directory already exists. 
    # If it already contains something, write_text() overwrites the existing content.
    Path(file_path).write_text(content, encoding="utf-8")



# Reads a JSON file.
# -> dict indicates that the function is expected to return a dictionary.
def read_json(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        # json.load(file) reads the JSON from the opened file and converts it into Python object.
        return json.load(file)




# Writes a dictionary to a JSON file.
def write_json(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as file:

        # json.dump() converts the Python data into JSON and writes it directly to the file.
        json.dump(data, file, indent=4)
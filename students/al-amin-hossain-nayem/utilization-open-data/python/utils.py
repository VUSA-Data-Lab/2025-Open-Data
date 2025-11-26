import json

def save_to_json(data, filename):
    """
    Saves a dictionary to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
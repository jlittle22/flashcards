# Configs

''' Path to JSON file containing flashcard set info with the format:
[
    {
        "name" : <name>,
        "cards" : [
            {
                "path" : <path to asset>,
                "type" : <asset type>,
                "key" : <correct answer>,
                "hint" : <OPTIONAL hint>,
            },
            ...
        ]
    },
    ...
]

<asset type> may be one of the following:

    IMAGE
'''
SETS_JSON_PATH = "sets.json"

import app
import json

def main():
    app.App(get_sets_configuration()).run()

def get_sets_configuration():
    with open(SETS_JSON_PATH, "r") as sets_file:
        return json.load(sets_file)

if __name__ == "__main__":
    main()

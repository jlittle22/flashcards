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

''' User guesses with a correctness score above or equal this threshold will be
counted as correct. See the `correctness_score` function in this file for a
precise definition.
'''
LEVENSHTEIN_THRESHOLD = 0.90

import json

def main():
    print(get_sets_configuration())

def get_sets_configuration():
    with open(SETS_JSON_PATH, "r") as sets_file:
        return json.load(sets_file)

def preprocess_key(guess):
    return guess.lower()

def is_guess_correct(guess, answer):
    return correctness_score > LEVENSHTEIN_THRESHOLD

def correctness_score(guess, answer):
    distance = levenshtein(guess, answer)
    return (len(answer) - distance) / answer

def levenshtein(a, b):
    if len(a) == 0:
        return len(b)
    
    if len(b) == 0:
        return len(a)

    if head(a) == head(b):
        return levenshtein(tail(a), tail(b))

    results = []

    results.append(levenshtein(a, tail(b)))
    results.append(levenshtein(tail(a), b))
    results.append(levenshtein(tail(a), tail(b)))

    return 1 + min(results)

def tail(string):
    return string[1:]

def head(string):
    return string[0]

if __name__ == "__main__":
    main()

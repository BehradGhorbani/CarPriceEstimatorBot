import json
def getPhrase(key, lang):
    with open('phrases.json') as file:
        data = json.load(file)

        return data[key][lang]
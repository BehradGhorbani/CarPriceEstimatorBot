import json
def getPhrase(key, lang):
    with open('src/i18n/phrases.json') as file:
        data = json.load(file)

        return data[key][lang]
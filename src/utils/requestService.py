from requests import get
from json import load

def getResponse(url):

    response = get(url)

    return response.json()
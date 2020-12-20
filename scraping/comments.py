from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from urllib.parse import urlencode
import json
import requests

API = 'ff46b59d4087e5bc1dbf65aa158e094b'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def return_sentiment(shcode):

    response = requests.get(get_url(f'https://www.instagram.com/p/{shcode}/?__a=1'))

    data = json.loads(response.content)

    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    sentim = []

    edges = data['graphql']['shortcode_media']['edge_media_preview_comment']['edges']

    for com in edges:
        # print(com['node']['text'])
        results = model.predict([com['node']['text']], k=len(com['node']['text']))
        for x in results:
            sentim.append(list(x.keys())[0])
    return sentim

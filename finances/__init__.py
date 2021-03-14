import requests as rq
from pprint import pp
from pyjson5 import decode
from .furls import beefy_urls


def Beefy():
    data = ""
    image_url = "https://github.com/beefyfinance/beefy-app/blob/master/src/images/"
    for url in beefy_urls['pools']:
        data += rq.get(url).text.split("=")[1][:-2]
    tokens = decode(data)
    for v in tokens:
        v['logo'] = image_url + v['logo'] + "?raw=true"
    return {x['earnContractAddress'].lower(): x for x in tokens}

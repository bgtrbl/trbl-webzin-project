import requests
from bs4 import BeautifulSoup


RANDOM_ARTICLE_URL = {
        'ko': 'http://ko.wikipedia.org/wiki/특수:임의문서',
        'en': 'http://en.wikipedia.org/wiki/Special:Random',
        'ja': 'http://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA',
        'fr': 'http://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard',
        }
LANGS = list(RANDOM_ARTICLE_URL.keys())

def get_random_doc(lang):
    resp = requests.get(RANDOM_ARTICLE_URL[lang])
    soup =  BeautifulSoup(resp.text)
    title = soup.find(id='firstHeading').string
    body = soup.find(id='mw-content-text')
    body.noscript.extract()
    tags = [ _.replace(" ", "_") for _ in soup.find(id='mw-normal-catlinks').ul.strings ]
    return {
            'title': title,
            'lang_title': "[{}] {}".format(lang, title),
            'body': body,
            'tags': tags,
            }


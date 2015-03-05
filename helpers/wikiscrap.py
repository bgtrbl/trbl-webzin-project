import requests
from bs4 import BeautifulSoup


# resource settings: lang -> url, pars
RESOURCES = {
        'ko': {
            'url': lambda : 'http://ko.wikipedia.org/wiki/특수:임의문서',
            'pars': lambda x: pars_wiki(x)},
        'en': {
            'url': lambda : 'http://en.wikipedia.org/wiki/Special:Random',
            'pars': lambda x: pars_wiki(x)},
        'ja': {
            'url': lambda : 'http://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA',
            'pars': lambda x: pars_wiki(x)},
        'fr': {
            'url': lambda : 'http://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard',
            'pars': lambda x: pars_wiki(x)},
        'io': {
            'url': lambda : 'http://io.wikipedia.org/wiki/Specala:HazardaPagino',
            'pars': lambda x: pars_wiki(x)},

        'enha': {
            'url': lambda : "https://mirror.enha.kr"+ \
                    BeautifulSoup(requests.get("https://mirror.enha.kr/random").text).meta.attrs['content'].split('=')[-1],
            'pars': lambda x: pars_enha(x)},
        }


LANGS = list(RESOURCES.keys())


def get_random_doc(lang):
    resp = requests.get(RESOURCES[lang]['url']())
    result =  RESOURCES[lang]['pars'](BeautifulSoup(resp.text))
    result['lang_title'] = '[{}] {}'.format(lang, result['title'])
    return result


# Custom Parsers

def pars_wiki(doc):
    title = doc.find(id='firstHeading').string
    body = doc.find(id='mw-content-text')
    body.noscript.extract()
    tags = [ _.replace(" ", "_") for _ in doc.find(id='mw-normal-catlinks').ul.strings ]
    tags += 'wiki'
    return {
            'title': title,
            'body': body,
            'tags': tags,
            }

def pars_enha(doc):
    title = doc.h1.string
    body = doc.article
    return {
            'title': title,
            'body': body,
            'tags': ['엔하'],
            }

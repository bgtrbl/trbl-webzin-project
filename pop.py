import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')
import django
django.setup()

from bgtrbl.apps.trblcms.models import Article, Sequel, Comment, Category
from bgtrbl.helpers import wikiscrap

from django.contrib.auth.models import User
from random import choice


def clear_article():
    print('clearing {} articles...'.format(len(Article.objects.all())))
    for i, v in enumerate(Article.objects.all()):
        print(i)
        v.delete()
    print("done")


def update_index():
    print('updating search index...')
    os.system('python3 manage.py update_index')
    print("done")


def wiki_scrap():
    # category lists
    CATS = (Category.objects.get(title='Wiki'),
            Category.objects.get(title='Magazin'),
            Category.objects.get(title='Forum'))

    #helper function
    def save_wiki(wikidoc):
        article = Article.objects.create(title=wikidoc['lang_title'],
                body=wikidoc['body'], user=choice(User.objects.all()),
                category=choice(CATS))
        article.tags.add(*wikidoc['tags'])
        return article

    count = int(input('Article count: '))

    while True:
        lang = input('language{}: '.format(wikiscrap.LANGS)).lower()
        if lang in wikiscrap.LANGS: break

    articles = []
    for _ in range(count):
        print("{}: Creating an article from a random wikipedia page...".format(_))
        articles.append(save_wiki(wikiscrap.get_random_doc(lang)))
        print("{}: {} has been created!!".format(_, articles[-1]))

    print("Created Articles:")
    print(articles)
    update_index()


def help_msg():
    msg = "Command List:\n"
    msg += "  (총 {} 개 커맨드)\n\n".format(len(COMMANDS))
    for k, v in COMMANDS.items():
        msg += "  {} \n\t- {}\n".format(k, v['desc'])
    print(msg)


COMMANDS = {}
COMMANDS['clear'] = {'func': clear_article, 'desc': '아티클 전체 삭제'}
COMMANDS['index'] = {'func': update_index, 'desc': '서치 인덱싱'}
COMMANDS['create'] = {'func': wiki_scrap, 'desc': 'Wikipidea 아티클 스크래핑'}
COMMANDS['quit'] = {'func': lambda : exit(), 'desc': '종료'}
COMMANDS['?'] ={'func': help_msg, 'desc': '도움말'}


if __name__ == '__main__':

    while True:
        try:
            COMMANDS[input('\n# ')]['func']()
        except KeyError:
            print("command not found - type '?' to see commands")

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')
import django
django.setup()

from bgtrbl.apps.trblcms.models import Article, Sequel, Comment, Category
from helpers import wikiscrap

from django.contrib.auth.models import User
from random import choice


def update_index():
    print('updating search index...')
    os.system('python3 manage.py update_index')
    print("done")


def clear_article():
    print('clearing {} articles...'.format(len(Article.objects.all())))
    for i, v in enumerate(Article.objects.all()):
        print(i)
        v.delete()
    print("done")
    update_index()


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

    #getting inputs
    while True:
        try:
            count = int(input('Article count: '))
            lang = input('language{}: '.format(wikiscrap.LANGS)).lower()
            if lang not in wikiscrap.LANGS:
                raise ValueError
        except ValueError:
            print("wrong input")
            continue
        except KeyboardInterrupt:
            print()
            return
        break

    articles = []
    for _ in range(count):
        print("{}: Creating an article from a random wikipedia page...".format(_))
        articles.append(save_wiki(wikiscrap.get_random_doc(lang)))
        print("{}: {} has been created!!".format(_, articles[-1]))

    print("Created Articles:")
    print(articles)
    update_index()


def count_article():
    articles = Article.objects.all()
    print("Total {} article(s) are in the db".format(len(articles)))


def help_msg():
    msg = "Command List:\n"
    msg += "  (총 {} 개 커맨드)\n\n".format(len(COMMANDS))
    for k, v in COMMANDS.items():
        msg += "  {} \n\t- {}\n".format(k, v['desc'])
    print(msg)

def quit_pop():
    raise KeyboardInterrupt

COMMANDS = {}
COMMANDS['clear'] = {'func': clear_article, 'desc': '아티클 전체 삭제'}
COMMANDS['index'] = {'func': update_index, 'desc': '서치 인덱싱'}
COMMANDS['create'] = {'func': wiki_scrap, 'desc': 'Wikipidea 아티클 스크래핑'}
COMMANDS['count'] = {'func': count_article, 'desc': '아티클 카운트 정보'}
COMMANDS['quit'] = {'func': quit_pop, 'desc': '종료'}
COMMANDS['?'] ={'func': help_msg, 'desc': '도움말'}


if __name__ == '__main__':

    while True:
        try:
            COMMANDS[input('\n# ')]['func']()
        except KeyError:
            print("command not found - type '?' to see commands")
        except KeyboardInterrupt:
            print("\nbye~")
            exit()

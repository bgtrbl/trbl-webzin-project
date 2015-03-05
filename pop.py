import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')

print("setting up django ...")

import django
django.setup()

print("importing apps ...")
from bgtrbl.apps.trblcms.models import Article, Sequel, Comment, Category
from django.contrib.auth.models import User

from helpers import wikiscrap
from random import choice
import subprocess
import datetime
import time
import signal
import psutil


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

    # helper function
    def save_wiki(wikidoc):
        article = Article.objects.create(title=wikidoc['lang_title'],
                body=wikidoc['body'], user=choice(User.objects.all()),
                category=choice(CATS))
        article.tags.add(*wikidoc['tags'])
        return article

    # getting inputs
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
    msg = "pop.py command list:\n"
    msg += "  (총 {} 개 커맨드)\n\n".format(len(COMMANDS))
    for k, v in COMMANDS.items():
        msg += "  {} -  {}\n".format(k.ljust(16), v['desc'])
    print(msg)


# exiting script
def quit_pop():
    print("\nbye~")
    # deleting server
    del globals()['SVR']
    exit()


class Server(object):
    def __init__(self):
        self.PROC = None

    def __del__(self):
        if self.is_runing():
            self.kill()

    def is_runing(self):
        return self.PROC is not None and self.PROC.poll() is None

    def status(self):
        if self.is_runing():
            print("server is currently running")
            print("PID: {}".format(self.PROC.pid))
        else:
            print("no server is currently running")

    def run(self):
        if self.is_runing():
            self.kill()
        print("starting server...")
        self.PROC = subprocess.Popen(['python3', 'manage.py', 'runserver', '0.0.0.0:8000'], shell=False)

    def kill(self):
        if self.is_runing():
            root = psutil.Process(self.PROC.pid)
            for child in root.children(recursive=True):
                child.kill()
            print("terminating server...")
            while self.PROC.poll() is None:
                time.sleep(0.5)
            self.PROC = None
        else:
            print("error: no server is running")



if __name__ == '__main__':

    SVR = Server()
    COMMANDS = {}
    COMMANDS['clear'] = {'func': clear_article, 'desc': '아티클 전체 삭제'}
    COMMANDS['index'] = {'func': update_index, 'desc': '서치 인덱싱'}
    COMMANDS['create'] = {'func': wiki_scrap, 'desc': 'Wikipidea 아티클 스크래핑'}
    COMMANDS['count'] = {'func': count_article, 'desc': '아티클 카운트 정보'}
    COMMANDS['quit'] = {'func': quit_pop, 'desc': '종료'}
    COMMANDS['run'] = {'func': SVR.run,
                        'desc': '서버 실행 -> python3 manage.py runserver 0.0.0.0:8000'}
    COMMANDS['kill'] = {'func': SVR.kill, 'desc': 'kill server'}
    COMMANDS['svr'] = {'func': SVR.status, 'desc': 'server status'}
    COMMANDS['?'] ={'func': help_msg, 'desc': '도움말'}

    while True:
        try:
            COMMANDS[input('\n# ')]['func']()
        except KeyError:
            print("command not found - type '?' to see commands")
        except KeyboardInterrupt:
            COMMANDS['quit']['func']()

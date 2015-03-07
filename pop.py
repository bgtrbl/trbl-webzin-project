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


def clear_article():
    narticles = Article.objects.count()
    print('clearing {} articles...'.format(narticles))
    count = 0
    try:
        while Article.objects.exists():
            Article.objects.last().delete()
            count += 1
            print("[{}] / {}".format(count, narticles-count))
    except KeyboardInterrupt:
        print('interrupted')
        return
    print("deleted {} articles".format(count))


def wiki_scrap():
    # category lists
    CATS = Category.objects.filter(level=2)

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
    try:
        for _ in range(count):
            print("{}: Creating an article from a random wikipedia page...".format(_))
            articles.append(save_wiki(wikiscrap.get_random_doc(lang)))
            print("{}: {} has been created in {}!!".format(_, articles[-1], articles[-1].category))
    except KeyboardInterrupt:
        print("interrupted")
        return

        print("Created Articles:")
        print(articles)
        print('to update index, run "index" command')


def count_objects():
    import bgtrbl.settings
    print("counting objects...")
    counts = (
        ('Categories', Category.objects.count()),
        ('Sequels', Sequel.objects.count()),
        ('Articles', Article.objects.count()),
        ('Comments', Comment.objects.count()),
        ('Tags', Article.tags.count()),
    )
    print("db: {}@{}".format(bgtrbl.settings.DATABASES['default']['NAME'],
        bgtrbl.settings.DATABASES['default']['HOST']))
    for model in counts:
        print("  [{}] {}".format(model[1], model[0]))


def help_msg(verbose=False):
    keys = list(COMMANDS.keys())
    keys.sort()

    msg = "pop.py command list:\n"
    if verbose:
        msg += "  (총 {} 개 커맨드)\n".format(len(COMMANDS))
    msg += '\n'
    for k in keys:
        msg += "  {} -  {}\n".format(k.ljust(16), COMMANDS[k]['desc'])
    if verbose:
        msg += "\n  Semicolon 으로 명령어 체이닝:"
        msg += "\n     (ex) # create;index;run\n"
        msg += "\n  ! 로 shell 명령 실행:"
        msg += "\n     (ex) # !ps"
        msg += "\n          # !kill <pid>"
        msg += "\n          # !git tree\n"

    print(msg)


class Server(object):
    def __init__(self):
        self.PROC = None

    def is_running(self):
        return self.PROC is not None and self.PROC.poll() is None

    def status(self):
        if self.is_running():
            print("server is currently running")
            print("PID: {}".format(self.PROC.pid))
        else:
            print("no server is currently running")

    def run(self):
        if self.is_running():
            self.kill()
        print("starting server...")
        self.PROC = subprocess.Popen(['python3', 'manage.py', 'runserver', '0.0.0.0:8000'], shell=False)

    def kill(self):
        if self.is_running():
            _kill_children(self.PROC)
            print("terminating server...")
            while self.PROC.poll() is None:
                time.sleep(0.5)
            self.PROC = None
        else:
            print("error: no server is running")


def show_tree():
    tree_command = ['tree', '-C', '-I', '"migrations|__pycache__|static|media|whoosh_index|__init__.py"']
    tree = subprocess.Popen(tree_command, stdout=subprocess.PIPE)
    less = subprocess.Popen('less', stdin=tree.stdout)
    less.wait()


def run_shell():
    print("starting django shell...")
    _excute('python3 manage.py shell')


def _kill_children(proc):
    root = psutil.Process(proc.pid)
    for child in root.children(recursive=True):
        child.terminate()


def _excute(shell_command):
    try:
        proc = subprocess.Popen(shell_command.split(), shell=False)

    except IndexError and FileNotFoundError:
        print("command error")
        return

    if 'proc' in locals():
        while proc.poll() is None:
            try:
                proc.wait()
            except KeyboardInterrupt:
                print("ignoring keyboard interrupt")
                pass


def quit_pop():
    # deleting server
    if globals()['SVR'].is_running():
        globals()['SVR'].kill()
    print("\nbye~")
    exit()


if __name__ == '__main__':

    SVR = Server()
    COMMANDS = {}
    COMMANDS['clear'] = {'func': clear_article, 'desc': '아티클 전체 삭제'}
    COMMANDS['index'] = {'func': update_index, 'desc': '서치 인덱싱'}
    COMMANDS['create'] = {'func': wiki_scrap, 'desc': 'Wikipidea 아티클 스크래핑'}
    COMMANDS['count'] = {'func': count_objects, 'desc': 'db objects count info'}
    COMMANDS['quit'] = {'func': quit_pop, 'desc': '종료'}
    COMMANDS['run'] = {'func': SVR.run, 'desc': '서버 실행 -> 0.0.0.0:8000'}
    COMMANDS['kill'] = {'func': SVR.kill, 'desc': 'kill server'}
    COMMANDS['svr'] = {'func': SVR.status, 'desc': 'server status'}
    COMMANDS['?'] ={'func': help_msg, 'desc': '도움말'}
    COMMANDS['??'] ={'func': lambda : help_msg(verbose=True), 'desc': '상세 도움말'}
    COMMANDS['tree'] ={'func': show_tree, 'desc': '프로젝트 트리'}
    COMMANDS['shell'] ={'func': run_shell, 'desc': 'Django shell'}
    COMMANDS['ts'] ={'func': lambda : _excute('tig status'),
            'desc': 'tig status'}
    COMMANDS['gs'] ={'func': lambda: _excute('git status'),
            'desc': 'git status'}


    while True:
        try:
            prompt = '\n{}> '.format(['OFF','ON'][SVR.is_running()])
            cmds = input(prompt)
            if cmds.startswith('!'):
                _excute(cmds[1:])
            else:
                for count, cmd in enumerate(cmds.split(';')):
                    COMMANDS[cmd.strip()]['func']()
                    print("[ {} ] done".format(count))
        except KeyError:
            print("command not found - type '?' to see commands")
        except KeyboardInterrupt:
            print()
            COMMANDS['quit']['func']()

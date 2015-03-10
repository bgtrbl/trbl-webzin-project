import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')

print("setting up django ...")

import django
django.setup()

print("importing apps ...")
from bgtrbl.apps.trblcms.models import Article, Sequel, Category
from bgtrbl.apps.trblcomment.models import Comment, CommentThread
from django.contrib.auth.models import User

from helpers import wikiscrap
from random import choice, sample, randrange
import subprocess
import datetime
import time
import signal
import psutil


def update_index():
    print('updating search index...')
    os.system('python3 manage.py update_index')


def clear_objects(o):
    n = o.objects.count()
    print('clearing {} {}...'.format(n, o))
    count = 0
    try:
        while o.objects.exists():
            o.objects.last().delete()
            count += 1
            print("[{}] / {}".format(count, n-count))
    except KeyboardInterrupt:
        print('interrupted')
        return
    print("deleted {} {}".format(count, o))


def wiki_scrap():
    # category lists
    CATS = Category.objects.filter(level=2)

    # helper function
    def save_wiki(wikidoc, c, u):
        c = Category.objects.get(title=c) if c else choice(CATS)
        u = User.objects.get(username=u) if u else choice(User.objects.all())

        article = Article.objects.create(title=wikidoc['lang_title'],
                body=wikidoc['body'], user=u,
                category=c)
        article.tags.add(*wikidoc['tags'])
        return article

    # getting inputs
    while True:
        try:
            count = int(input('Article count: '))

            lang = input('language[random] {}: '.format(wikiscrap.LANGS)).lower()
            if lang and lang not in wikiscrap.LANGS:
                raise KeyError

            cats = input('category[random] {}: '.format(CATS))
            if cats and not Category.objects.filter(title=cats).exists():
                raise KeyError

            user_name = input('user[random] : ')
            if user_name and not User.objects.filter(username=user_name).exists():
                raise KeyError

        except (ValueError, KeyError):
            print("wrong input")
            continue
        except KeyboardInterrupt:
            print()
            return
        break

    articles = []
    try:
        for _ in range(count):
            print("{}: Creating an article from a random page...".format(_))
            wikidoc = wikiscrap.get_random_doc(lang)
            if wikidoc:
                articles.append(save_wiki(wikidoc, cats, user_name))
                print("{}: {} has been created in {}!!".format(_, articles[-1], articles[-1].category))
            else:
                print("skipping...")
    except KeyboardInterrupt:
        print("interrupted")
        return

    print("Created Articles:")
    print(articles)
    print('to update index, run "index" command')


def create_sequel():
    while True:
        try: n = int(input('Sequel count: '))
        except ValueError: continue
        break

    sequels = []
    for trial in range(n):
        print('trial:', trial)
        user = choice(User.objects.all())
        print('selected user:', user)
        category = choice(Category.objects.filter(level=2))
        print('selected category:', category)

        # 아티클 가져오기
        print('getting articles ...')
        if not category.article_set.filter(category=category, sequel=None, user=user).exists():
            print('empty set returned, skipping ...')
            continue
        articles = category.article_set.filter(category=category, sequel=None, user=user).all()

        print('choosing ...', articles)
        # 랜덤으로 아티클 뽑기
        if len(articles) != 1:
            articles = sample(list(articles), randrange(1, len(articles)))
        # 시퀄 만들기
        print('createing a sequel ...')
        _a = choice(articles)
        title = '[seq] {}'.format(_a.title)
        description = '<img src="{}" art="sequel-image">'.format(_a.get_header_img()['src'])
        sequel = Sequel.objects.create(user=user, title=title,
                                    description=description, category=category)
        for a in articles:
            a.sequel = sequel
            a.save()

        print('{} sequel saved'.format(sequel))
        print('\t related articles: {}'.format(sequel.article_set.all()))
        sequels.append(sequel)

    if sequels:
        print('\ncreated {} sequels: {}'.format(len(sequels), sequels))
    else:
        print('\nno sequel created')


def count_objects():
    import bgtrbl.settings
    print("counting objects...")
    counts = (
        ('Categories', Category.objects.count()),
        ('Sequels', Sequel.objects.count()),
        ('Articles', Article.objects.count()),
        ('Comments', Comment.objects.count()),
        ('Comment threads', CommentThread.objects.count()),
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


def db_info():
    import bgtrbl.settings
    print("DB  : {}".format(bgtrbl.settings.DATABASES['default']['NAME']))
    print("USER: {}".format(bgtrbl.settings.DATABASES['default']['USER']))
    print("HOST: {}".format(bgtrbl.settings.DATABASES['default']['HOST']))
    print("NAME: {}".format(bgtrbl.settings.DATABASES['default']['PORT']))


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
    COMMANDS['clr_a'] = {'func': lambda : clear_objects(Article), 'desc': '아티클 전체 삭제'}
    COMMANDS['clr_s'] = {'func': lambda : clear_objects(Sequel), 'desc': '시퀄 전체 삭제'}
    COMMANDS['clr_c'] = {'func': lambda : clear_objects(Comment), 'desc': '댓글 전체 삭제'}
    COMMANDS['clr_t'] = {'func': lambda : clear_objects(CommentThread), 'desc': '쓰레드 전체 삭제'}
    COMMANDS['clr'] = {'func': lambda : [clear_objects(_) for _ in (Article, Sequel, Comment, CommentThread)], 'desc': '다 삭제'}
    COMMANDS['index'] = {'func': update_index, 'desc': '서치 인덱싱'}
    COMMANDS['db'] = {'func': db_info, 'desc': 'Database info'}
    COMMANDS['crt'] = {'func': wiki_scrap, 'desc': 'Wikipidea 아티클 스크래핑'}
    COMMANDS['crt_s'] = {'func': create_sequel, 'desc': '랜덤 시퀄링'}
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

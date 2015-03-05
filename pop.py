import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')
import django
django.setup()

from bgtrbl.apps.trblcms.models import Article, Sequel, Comment, Category
from bgtrbl.helpers import wikiscrap

from django.contrib.auth.models import User
from random import choice


cats = (Category.objects.get(title='Wiki'),
        Category.objects.get(title='Magazin'),
        Category.objects.get(title='Forum'))


def save_wiki(wikidoc):
    article = Article.objects.create(title=wikidoc['title'],
            body=wikidoc['body'], user=choice(User.objects.all()),
            category=choice(cats))
    article.tags.add(*wikidoc['tags'])
    return article

if __name__ == '__main__':
    count = int(input('Article count: '))

    while True:
        lang = input('language[{}]: '.format(wikiscrap.LANGS)).lower()
        if lang in wikiscrap.LANGS: break

    articles = []
    for _ in range(count):
        print("{}: Creating an article from a random wikipedia page...".format(count))
        articles.append(save_wiki(wikiscrap.get_random_doc(lang)))
        print("{}: {} has been created!!".format(_, articles[-1]))

    print("Created Articles:")
    print(articles)

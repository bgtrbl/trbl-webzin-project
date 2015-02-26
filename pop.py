import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bgtrbl.settings')
import django
django.setup()

from bgtrbl.apps.trblcms.models import Article, Sequel, Comment, Category

# 사이트 구조 예시
ROOT = Category.objects.create(title="root")
MAGAZIN = Category.objects.create(title="Magazin", parent=ROOT)
FORUM = Category.objects.create(title="Forum", parent=ROOT)

REVIEWS = Category.objects.create(title="Reviews", parent=MAGAZIN)
TUTORIALS = Category.objects.create(title="Tutorials", parent=MAGAZIN)
GALLERY = Category.objects.create(title="Gallery", parent=FORUM)
WIKI = Category.objects.create(title="Wiki", parent=FORUM)

# Test articles and sequels
article = Article.objects.create(title="Webzin Launching!!", body="v 0.0.1", category=ROOT)
article.tags.add("launching!", "webzin", "notice")
notice_sequel = Sequel.objects.create(title="Notice", description="Notices are here!", category=article.category)
article.sequel = notice_sequel
article.save()

article = Article.objects.create(title="Notice test 1", body="notice body", category=ROOT)
article.tags.add("notice")
article.sequel = notice_sequel
article.save()

article = Article.objects.create(title="Magazin Test Article", body="good magazin", category=MAGAZIN)
article.tags.add("test", "webzin")

article = Article.objects.create(title="Something Review", body="a review body", category=REVIEWS)
article.tags.add("test", "something", "review")

article = Article.objects.create(title="Something Tutorial", body="a tutorial body", category=TUTORIALS)
article.tags.add("test", "something", "tutorial", "random_tag1")

article = Article.objects.create(title="Something Artwork", body="a art body", category=GALLERY)
article.tags.add("test", "something", "Artwork", "random_tag1", "pony")

article = Article.objects.create(title="Wikipage about something", body="a something body", category=WIKI)
article.tags.add("test", "something")

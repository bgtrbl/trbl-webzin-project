from django.test import TestCase
from .models import Article, Sequel, Category


# 작성중...
class TrblCmsTestCase(TestCase):
    def setUp(self):
        # Category Setup
        self.TestCategory = Category.objects.create(title="root")

        article = Article.objects.create(title="Test Article 1 in Sequel"
                body="good sequel", category=self.TestCategory)
        article.tags.add("launching!", "webzin", "test")
        sequel = Sequel.objects.create(title="Test Sequel", description="Test
                Sequel", category=article.category)
        article.sequel = sequel
        article.save()
        article = Article.objects.create(title="Test Article 2 in Sequel"
                body="good sequel", category=self.TestCategory)
        article.tags.add("launching!", "webzin", "test")
        article.sequel = sequel
        article.save()


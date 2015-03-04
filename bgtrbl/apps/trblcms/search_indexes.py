import datetime
from haystack import indexes
from bgtrbl.apps.trblcms.models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # document=True convention: name the field "text"
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

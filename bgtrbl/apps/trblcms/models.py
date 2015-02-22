from django.db import models

from taggit.managers import TaggableManager
from uuslug import uuslug

from ckeditor.fields import RichTextField


# abstract class to factor out repeated parts
class BaseItemModel(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    # @todo make the method bypass-able to set slug explicitly (for admins)
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, start_no=2,
                           max_length=200, word_boundary=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


# @& manager
class Category(BaseItemModel):
    level = models.IntegerField(default=0)
    public = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)


# Sequence 보다 Sequel이 더 맞는것 같아서 이름을 Sequel 로 함
# @& QuerySet
class Sequel(BaseItemModel):
    # @todo user
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # @todo category - returns category key from any item in it

    # @? True 시 다른유저도 Sequel 에 추가 가능?
    public = models.BooleanField(default=False)

    def category(self):
        return self.article_set.last().category

    class Meta(BaseItemModel.Meta):
        ordering = ["-created_at"]


# Article model's custom query set to customize default 'objects' manager
class ArticleQuerySet(models.QuerySet):
    def published(self, value=True):
        return self.filter(published=value)


class Article(BaseItemModel):
    # @todo user
    body = RichTextField(config_name='article_body')
    # Sequel 삭제시 foreign key null
    sequel = models.ForeignKey(Sequel, blank=True, null=True,
                               on_delete=models.SET_NULL)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    # @! category blankable/nullable for testing
    category = models.ForeignKey(Category, blank=True, null=True)

    # applying custom query set as manager
    objects = ArticleQuerySet.as_manager()

    class Meta(BaseItemModel.Meta):
        ordering = ["-created_at"]

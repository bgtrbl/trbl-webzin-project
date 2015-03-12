from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from uuslug import uuslug
from bgtrbl.apps.trblcomment.models import CommentedItemMixin

from ckeditor.fields import RichTextField

from .helpers import get_visible_string

from bs4 import BeautifulSoup

# baseclass -> mixin class
class SluggedItemMixin(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    # @todo make the method bypass-able to set slug explicitly (for admins)
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self, start_no=2, max_length=200, word_boundary=True)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# @& manager
# 상위레벨에서 정리하는 단위:
#   (포럼 카테고리[level0]->유저 연제물 카테고리[level1])
#   (웸진 카테고리[level0] -> 강좌 카테고리[level1])
# models.Model 상속으로 수정 예정
# no slug
class Category(SluggedItemMixin):
    level = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    public = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True)

    def get_children(self):
        return self._default_manager.filter(parent=self)

    def get_descendants(self):
        desc = set(self.get_children())
        for node in list(desc):
            desc.update(node.get_descendants())
        return desc

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.title, self.level)


# Article model's custom query set to customize default 'objects' manager
class ArticleSequelQuerySet(models.QuerySet):
    def get_recent_iterator(self):
        return self.order_by('-created_at').iterator()

    def get_recent(self, n):
        result = []
        i = get_recent_iterator()
        for _ in range(n):
            try:
                result.append(next(i))
            except StopIteration:
                break
        return result


# @? signal based count?
class Sequel(SluggedItemMixin, CommentedItemMixin):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    # @todo user
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)

    # @? True 시 다른유저도 Sequel 에 추가 가능?
    public = models.BooleanField(default=False)

    objects = ArticleSequelQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('trblcms:sequel_detail', kwargs={'slug': self.slug})

    #def get_edit_url(self):

    def __str__(self):
        return "{}: {}".format(self.title, self.category)

    class Meta:
        ordering = ["-created_at"]


class Article(SluggedItemMixin, CommentedItemMixin):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    # @todo user
    body = RichTextField()
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
    objects = ArticleSequelQuerySet.as_manager()


    # save method override 해서 url field에 헤더이미지 추가하는 로직작성 예정
    # 지금은 그냥 첫번째 이미지를 가져옴
    def get_header_img(self):
        try:
            return self._img_tags().pop(0).attrs
        except IndexError:
            pass

        return None

    def _img_tags(self):
        return BeautifulSoup(self.body).find_all('img')

    # 짧은 바디 줌
    def get_body_string(self):
        body_text_tags = BeautifulSoup(self.body).findAll(text=True)
        return get_visible_string(body_text_tags)

    def get_absolute_url(self):
        return reverse('trblcms:article_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return "{}: {}".format(self.title, self.category)

    class Meta:
        ordering = ["-created_at"]

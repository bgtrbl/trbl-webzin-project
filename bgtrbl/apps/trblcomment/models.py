from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# @todo override save and create thread after save
class CommentThread(models.Model):
    def __str__(self):
        # @! temporary id return
        return str(self.id)


# possible commented item(with CommentedItemMixin) for tree style commenting
class Comment(models.Model):
    # @todo user
    # comment 는 마지막 변경시간만 가지고 있음
    date = models.DateTimeField(auto_now=True)
    # optional author submission
    user = models.ForeignKey(User)
    text = models.TextField()
    parent_thread = models.ForeignKey(CommentThread)

    def __str__(self):
        return "{}: {}".format(self.parent_thread, self.text[:80])

    class Meta:
        ordering = ["date"]


# @? commentedItem mixin?, signal?
# @? maybe it can store parent information such as type
class CommentedItemMixin(models.Model):
    # possible OneToOne field
    # @! nullable blankable testing
    child_thread = models.ForeignKey(CommentThread, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.child_thread = CommentThread.objects.create()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

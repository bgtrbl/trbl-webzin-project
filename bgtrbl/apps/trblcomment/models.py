from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# @todo override save and create thread after save
class CommentThread(models.Model):
    def __str__(self):
        # @! temporary id return
        return str(self.id)


class CommentQuerySet(models.QuerySet):
    def get_recent(self, n):
        result = []
        i = self.order_by('-modified_at').iterator()
        for _ in range(n):
            try:
                result.append(next(i))
            except StopIteration:
                break
        return result


# possible commented item(with CommentedItemMixin) for tree style commenting
class Comment(models.Model):
    # @todo user
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # optional author submission
    user = models.ForeignKey(User)
    text = models.CharField(max_length=200, blank=False, null=False)
    parent_thread = models.ForeignKey(CommentThread)

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return "{}: {}".format(self.parent_thread, self.text[:80])

    class Meta:
        ordering = ["created_at"]


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

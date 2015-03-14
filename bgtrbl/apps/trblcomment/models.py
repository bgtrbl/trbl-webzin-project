from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

from .score import ci

# @todo override save and create thread after save
class CommentThread(models.Model):
    def __str__(self):
        # @! temporary id return
        return str(self.id)


class CommentQuerySet(models.QuerySet):
    # @n togoaway
    def get_recent(self, n):
        return self.order_by('-modified_at')
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
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0.0)

    objects = CommentQuerySet.as_manager()
    vote = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vote = None

    def _scoring(self):
        if self.vote is not None:
            if self.vote:
                self.up_votes += 1
            else:
                self.down_votes += 1
            self.score = ci(self.up_votes, self.up_votes+self.down_votes)

    def save(self, *args, **kwargs):
        self._scoring()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}: score({})".format(self.parent_thread, self.text[:80], self.score)

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

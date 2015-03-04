from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# @& 1-1 model - django's auth or allauth, multitable inheritance
# @togoaway image field 지울 예정 (avatar로 대체)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = RichTextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    # True = female; False = male  -> for gender equality ...
    gender = models.NullBooleanField(default=None)
    # @? other social variables?
    website = models.URLField(blank=True, unique=True, null=True)

    def get_absolute_url(self):
        return reverse('userprofile:userprofile_detail',kwargs={'pk':self.id})

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)

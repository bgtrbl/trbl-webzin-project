from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


# @& 1-1 model - django's auth or allauth, multitable inheritance
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #image = models.ImageField()
    bio = RichTextField(blank=True)
    dob = models.DateField(blank=False)
    # True = female; False = male  -> for gender equality ...
    gender = models.NullBooleanField(default=None)
    # @? other social variables?
    website = models.URLField(blank=True, unique=True)

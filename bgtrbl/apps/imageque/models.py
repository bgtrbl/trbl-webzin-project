from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=80, blank=True, null=True)
    image_file = models.ImageField()

    # @todo url
    def get_absolute_url(self):
        return #reverse('userprofile:userprofile_detail',kwargs={'pk':self.id})

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

class ImagequeMixin(models.Model):
    images = models.ManyToManyField(Image)

    class Meta:
        abstract = True

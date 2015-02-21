from django.contrib import admin
from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "modified_at", "published")

admin.site.register(models.Article, ArticleAdmin)

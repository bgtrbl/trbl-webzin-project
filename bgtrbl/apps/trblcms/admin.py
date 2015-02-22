from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("level", "parent", "title", "public")


class SequelAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "created_at")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "modified_at", "published")


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Sequel, SequelAdmin)
admin.site.register(models.Article, ArticleAdmin)

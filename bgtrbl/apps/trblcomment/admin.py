from django.contrib import admin
from . import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ("parent_thread", "user", "text")


admin.site.register(models.Comment, CommentAdmin)

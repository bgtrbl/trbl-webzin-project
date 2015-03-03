from django.contrib import admin
from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dob",)


admin.site.register(models.UserProfile, UserProfileAdmin)

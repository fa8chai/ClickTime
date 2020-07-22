from django.contrib import admin


# Register your models here.

from .models import Profile, UserFollowing, UserBlocking

admin.site.register(Profile)
admin.site.register(UserBlocking)
admin.site.register(UserFollowing)

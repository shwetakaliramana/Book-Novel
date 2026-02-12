from django.contrib import admin

from userapp.models import UserActivity, UserProfile

# Register your models here
admin.site.register(UserActivity)
admin.site.register(UserProfile)

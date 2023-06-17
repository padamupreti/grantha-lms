from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import LMSUser

admin.site.register(LMSUser, UserAdmin)

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from schoolcorp_app.models import CustomUser


# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
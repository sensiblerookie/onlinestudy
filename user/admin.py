from django.contrib import admin
from user.models import User
#
#
# # Register your models here.
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['userName', 'password', 'fullName', 'sex', 'userPhone', 'userEmail', 'is_staff', 'is_active',
#                     'createTime', 'loginLastTime', ]
#
#
# admin.site.register(User, UserAdmin)
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(User, UserProfileAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Account

admin.site.unregister(User)


@admin.register(Account)
class AccountAdmin(UserAdmin):
    pass
from .models import Post


admin.site.register(Post)

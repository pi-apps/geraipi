from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from store.models import Expedisi, UserStore, UserStoreAddress

from .forms import UserStoreForm


# Register your models here.
class UserStoreAdmin(admin.ModelAdmin):
    form = UserStoreForm


admin.site.register(UserStore, UserStoreAdmin)
admin.site.register(UserStoreAddress)
admin.site.register(Expedisi)

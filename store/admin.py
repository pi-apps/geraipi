from django.contrib import admin
from store.models import UserStore, UserStoreAddress, Expedisi
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from typing import Any
from .forms import UserStoreForm

# Register your models here.
class UserStoreAdmin(admin.ModelAdmin):
    form = UserStoreForm

admin.site.register(UserStore, UserStoreAdmin)
admin.site.register(UserStoreAddress)
admin.site.register(Expedisi)

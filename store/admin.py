from django.contrib import admin

from master.models.expedisi import Expedisi
from store.models import UserStore, UserStoreAddress

from .forms import UserStoreForm


# Register your models here.
class UserStoreAdmin(admin.ModelAdmin):
    list_display = ["users", "nama", "coin", "is_active_store", "aggrement"]
    search_fields = ["users__username", "nama"]
    form = UserStoreForm


admin.site.register(UserStore, UserStoreAdmin)
admin.site.register(UserStoreAddress)
admin.site.register(Expedisi)

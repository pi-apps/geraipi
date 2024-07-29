from django.shortcuts import render

from profiles.models import UserSettingsMember
from store.models import UserStore

from ..base_view import FrontPage


class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        if request.user.is_anonymous:
            profile = None
        profile_setting = UserSettingsMember.objects.get(user=profile)
        stores = UserStore.objects.get(users_id=profile.id)
        is_registered = False
        if profile_setting:
            is_registered = True
        datas = {
            "status_pesanan": pesanan,
            "profile": profile,
            "registered": is_registered,
            "settings": profile_setting,
            "stores": stores
        }
        return render(request, "profil/profile.html", datas)

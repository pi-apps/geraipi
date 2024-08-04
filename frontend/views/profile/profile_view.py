from django.shortcuts import render

from profiles.models import UserSettingsMember
from store.models import UserStore

from ..base_view import FrontPage


class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        datas = None
        if request.user.is_authenticated:
            if request.user.is_anonymous:
                profile = None
            profile_setting = UserSettingsMember.objects.filter(
                user_id=profile.id
            ).last()
            stores = UserStore.objects.filter(users_id=profile.id).first()
            is_registered = False
            if profile_setting.tier:
                is_registered = True
            datas = {
                "status_pesanan": pesanan,
                "profile": profile,
                "registered": is_registered,
                "settings": profile_setting,
                "stores": stores,
            }
        return render(request, "profil/profile.html", datas)

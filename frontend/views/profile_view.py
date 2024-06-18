from django.shortcuts import render

from produk.models import Cart
from profiles.models import UserSettingsMember

from .base_view import FrontPage


class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        if request.user.is_anonymous:
            profile=None
        profile_setting = UserSettingsMember.objects.filter(user=profile)
        is_registered = False
        if profile_setting.exists():
            profile_setting = profile_setting.first()
            if profile_setting:
                is_registered = True
        datas = {"status_pesanan": pesanan, "profile": profile, "registered": is_registered}
        return render(request, "profil/profile.html", datas)

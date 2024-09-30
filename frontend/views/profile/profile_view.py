from django.shortcuts import render
from django.urls import reverse
from sesame.utils import get_query_string

from frontend.views.base_view import FrontPage
from profiles.models import UserSettingsMember
from store.models import UserStore


class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        datas = None
        url_data = reverse("log_less")
        if request.user.is_authenticated:
            if request.user.is_anonymous:
                profile = None
            else:
                url_data = url_data + get_query_string(profile)
            profile_setting = UserSettingsMember.objects.filter(user_id=profile.id).last()
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
                "url_data": request.build_absolute_uri(url_data),
            }
        return render(request, "profil/profile.html", datas)

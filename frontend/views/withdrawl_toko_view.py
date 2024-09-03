from django.shortcuts import render

from profiles.models import UserSettingsMember
from store.models import UserStore, UserStoreWdHistory

from .base_view import FrontPage


class WithdrawlToko(FrontPage):
    def get(self, request, id):
        toko = UserStore.objects.get(users_id=id)
        usersetting = UserSettingsMember.objects.get(user_id=request.user.id)
        historywd = UserStoreWdHistory.objects.all().order_by("-pk")
        kuotatersisa = usersetting.tier.kuota_withdrawl - usersetting.kuota
        is_premium = False
        if usersetting.tier:
            if usersetting.tier.kuota_withdrawl > 0:
                is_premium = True
        return render(
            request,
            "toko/withdrawl.html",
            {
                "toko": toko,
                "history": historywd,
                "setting": usersetting,
                "sisa_kuota": kuotatersisa,
                "premium": is_premium,
            },
        )

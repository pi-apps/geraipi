from django.shortcuts import render

from store.models import UserStore, UserStoreWdHistory

from .base_view import FrontPage


class WithdrawlToko(FrontPage):
    def get(self, request, id):
        toko = UserStore.objects.get(users_id=id)
        historywd = UserStoreWdHistory.objects.all().order_by("-pk")
        return render(
            request, "toko/withdrawl.html", {"toko": toko, "history": historywd}
        )

from django.db.models import Sum
from django.shortcuts import render

from profiles.models import (
    UserSettingsMember,
    UserWithdrawlTransaction,
    UserwithdrawlTransactionRequest,
)

from .base_view import FrontPage


class Withdrawl(FrontPage):
    def get(self, request):
        user = request.user
        history = UserWithdrawlTransaction.objects.filter(
            user_id=request.user.id
        ).order_by("-pk")
        history_request = UserwithdrawlTransactionRequest.objects.filter(
            user_id=request.user.id, status=1
        ).order_by("-pk")

        userwd = UserwithdrawlTransactionRequest.objects.filter(
            user_id=request.user.id, status=1
        )
        userwd = userwd.aggregate(total=Sum("jumlah"))
        userwd = userwd["total"] or 0

        total = user.coin - userwd

        usersetting = UserSettingsMember.objects.filter(user=request.user.id).first()

        return render(
            request,
            "user_withdrawl_user.html",
            {
                "users": user,
                "history": history,
                "history_request": history_request,
                "totals": total,
                "profiles": usersetting,
            },
        )

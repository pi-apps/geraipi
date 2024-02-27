from .base_view import FrontPage
from profiles.models import UserWithdrawlTransaction, UserwithdrawlTransactionRequest
from django.shortcuts import render
from django.db.models import Sum


class Withdrawl(FrontPage):
    def get(self, request):
        user = request.user
        history = UserWithdrawlTransaction.objects.filter(user_id=request.user.id).order_by('-pk')
        history_request = UserwithdrawlTransactionRequest.objects.filter(user_id=request.user.id, status=1).order_by("-pk")
        
        userwd = UserwithdrawlTransactionRequest.objects.filter(user_id=request.user.id, status=1)
        userwd = userwd.aggregate(total=Sum("jumlah"))
        userwd = userwd["total"] or 0
        
        total = user.coin - userwd
        
        return render(request, 'user_withdrawl_user.html',{"users":user, "history": history, "history_request":history_request, "totals":total})
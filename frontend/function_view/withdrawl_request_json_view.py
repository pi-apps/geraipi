from .base_view import FrontPage
from django.http import JsonResponse
from profiles.models import UserwithdrawlTransactionRequest, UserWithdrawlTransaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum


@method_decorator(csrf_exempt, name='dispatch')
class WithdrawlRequestJson(FrontPage):
    def post(self, request):
        data = {
            "success": False
        }
        gettype = request.POST.get("jumlah", 0)
        userwd = UserwithdrawlTransactionRequest.objects.filter(user_id=request.user.id, status=1)
        userwd = userwd.aggregate(total=Sum("jumlah"))
        userwd = userwd["total"] or 0
        
        if gettype:
            gettype = float(gettype)
            if gettype > 0.0:
                user = request.user
                usercoin = user.coin - userwd
                if usercoin > gettype:
                    try:
                        transaksi_request = UserwithdrawlTransactionRequest.objects.create(user_id=request.user.id, jumlah=gettype, status=1)
                        data.update({
                            "success":True,
                            "message": "Success add request"
                        })
                    except Exception as e:
                        data.update({
                            "success":False,
                            "message": "Fail add request"
                        })
                else:
                    data.update({
                        "success":False,
                        "message": "Not enought"
                    })
        else:
            data.update({
                "success":False,
                "message": "Not enought"
            })
        return JsonResponse(data)
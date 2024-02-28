from django.http import JsonResponse

from produk.models import CartItem

from .base_view import FrontPage


class TransaksiUserCountJson(FrontPage):
    def get(self, request):
        data = {"success": False}
        try:
            transaksi = CartItem.objects.filter(cart__user_id=request.user.id)
            data.update(
                {
                    "success": True,
                    "data": {
                        "pending": transaksi.filter(cart__status=1).count(),
                        "proses": transaksi.filter(cart__status=2).count(),
                        "dikirim": transaksi.filter(cart__status=3).count(),
                    },
                }
            )
        except Exception as e:
            print(e)
            data.update({"data": []})
        return JsonResponse(data)

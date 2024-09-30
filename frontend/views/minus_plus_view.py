from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from produk.models import CartItem

from .base_view import FrontPage


@method_decorator(login_required(login_url="/profile"), name="dispatch")
class MinusPluss(FrontPage):
    def get(self, request):
        data = None
        try:
            cart_data = CartItem.objects.filter(cart__user_id=request.user.id, cart__status=1).first()
            typerequest = request.GET.get("type_request")
            if typerequest == "plus":
                cart_data.jumlah = cart_data.jumlah + 1
            else:
                cart_data.jumlah = cart_data.jumlah - 1
            cart_data.save()
            data = {
                "nama_produk": cart_data.produk.nama,
                "jumlah": cart_data.jumlah,
                "harga": cart_data.produk.harga,
                "kategori": [c.id for c in cart_data.produk.kategori.all()],
            }
        except Exception as e:
            print(e)
            cart_data = None
        return JsonResponse({"data": data})

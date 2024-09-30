import calendar
import time

from django.http import JsonResponse

from produk.models import Cart, CartItem, Produk

from .base_view import FrontPage


class KeranjangAdd(FrontPage):
    def post(self, request, id=0):
        keranjang_item = CartItem.objects.filter(produk__pk=id, cart__user__pk=request.user.id)
        status = {"success": False}
        if keranjang_item:
            for k in keranjang_item:
                k.jumlah += 1
                k.save()
            status = {"success": True}
        else:
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            keranjang = Cart.objects.create(kode=str(time_stamp), user=request.user, status=1)
            produk = Produk.objects.get(pk=id)
            keranjang_item = CartItem.objects.create(cart=keranjang, produk=produk)
            status = {"success": True}

        return JsonResponse(status)

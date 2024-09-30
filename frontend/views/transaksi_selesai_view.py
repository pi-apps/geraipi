from django.http import JsonResponse

from frontend.views.base_view import FrontPage
from produk.models import Cart, CartItem
from store.models import UserStore


class TransaksiUserSelesaiJson(FrontPage):
    def get(self, request):
        cart_id = request.GET.get("cart_id", None)
        try:
            if cart_id:
                cartitem = CartItem.objects.get(pk=cart_id)

                carts = Cart.objects.get(pk=cartitem.cart.id)
                carts.status = 4
                carts.status_toko = 4
                carts.save()

                userprofile = UserStore.objects.get(pk=cartitem.produk.store.id)
                userprofile.coin += float(cartitem.jumlah) * float(cartitem.produk.harga)
                userprofile.save()
        except Exception as e:
            print(e)
        return JsonResponse({"success": True}, safe=False)

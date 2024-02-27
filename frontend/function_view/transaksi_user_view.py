from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from produk.models import Cart, CartItem

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
class TransaksiUsers(FrontPage):
    def get(self, request):
        userstore = Cart.objects.filter(
            user_id=request.user.id, status_pembayaran__gte=2
        )
        transaksi_status = {
            "pending": userstore.filter(status=1).count(),
            "diproses": userstore.filter(status=2).count(),
            "dikirim": userstore.filter(status=3).count(),
        }
        transaksi_data = userstore.filter(status=request.GET.get("status", 1))
        data = {
            "data": userstore,
            "transaksi": transaksi_status,
            "transaksi_data": transaksi_data,
        }
        return render(request, "profil/transaksi_user.html", data)

    def post(self, request):
        userstore = Cart.objects.filter(
            user_id=request.user.id, status_pembayaran__gte=2
        )
        userstore = userstore.filter(pk=request.POST.get("id")).first()
        userstore.status = 4
        userstore.status_toko = 4
        userstore.save()
        userstore_item = CartItem.objects.filter(cart_id=userstore.id).first()
        userstore_store = userstore_item.produk_chart.store
        userstore_store.coin = float(userstore_store.coin) + float(
            userstore_item.produk.harga
        )
        userstore_store.save()
        return redirect("/transaksi/users/list?status=" + request.GET.get("status"))

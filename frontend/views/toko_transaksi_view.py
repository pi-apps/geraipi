import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from produk.models import Cart, CartItem
from store.models import Expedisi, UserStore

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class TransaksiToko(FrontPage):
    def post(self, request, id):
        status = request.GET.get("status", 1)
        if status:
            cart = Cart.objects.get(pk=request.POST.get("cart_id"))
            # for c in cart:
            if cart.status_toko == 1:
                cart.status_toko = 2
                cart.status = 2
            elif cart.status_toko == 2:
                resi = request.POST.get("nomor_resi").strip()
                layanan = request.POST.get("expedisi").strip()
                if resi and layanan:
                    cart.nomor_resi = resi
                    cart.tanggal_dikirim = datetime.datetime.now()
                    cart.status_toko = 3
                    cart.status = 3
                    cart.expedisi_id = request.POST.get("expedisi")
                else:
                    messages.error(request, "Sorry, please input your number")
                    return redirect(
                        reverse(
                            "transaksi_toko",
                            kwargs={"id": str(request.user.id)},
                        )
                        + "?status="
                        + str(status)
                    )
            elif cart.status_toko == 3:
                cart.status = 3
                cart.tanggal_selesai = datetime.datetime.now()
                # cart.status_toko = 4
            cart.save()
        return redirect("/toko/" + str(request.user.id) + "/transaksi/")

    def get(self, request, id):
        expedisi = Expedisi.objects.all()
        context = {
            "produk": None,
            "expedisi": expedisi,
            "pesanan": 0,
            "diproses": 0,
            "dikirim": 0,
        }
        status = request.GET.get("status", 1)
        store = UserStore.objects.get(users_id=request.user.id)
        if status:
            produk = CartItem.objects.filter(
                # cart__user_id=request.user.id,
                cart__status_toko=status,
                produk__store_id=store.id,
                cart__status_pembayaran=2,
            )
            context.update({"produk": produk})
        context.update(
            {
                "pesanan": CartItem.objects.filter(
                    cart__status_toko=1,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
                "diproses": CartItem.objects.filter(
                    cart__status_toko=2,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
                "dikirim": CartItem.objects.filter(
                    cart__status_toko=3,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
            }
        )
        return render(request, "toko/listtransaksi.html", context)

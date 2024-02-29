from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.function_view.base_view import FrontPage
from produk.models import Cart, CartItem, UlasanCart


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class DetailTransaksiUlasan(FrontPage):
    def post(self, request, id):
        cart = Cart.objects.get(pk=id)
        cartitem = CartItem.objects.get(cart_id=cart.id)
        ulasan = UlasanCart.objects.filter(cart_id=id).first()
        if not ulasan:
            ulasan = UlasanCart()
        ulasan.produk = request.POST.get("rating_produk", 0)
        ulasan.catatan = request.POST.get("catatan_produk", "-")
        ulasan.cart = cart
        ulasan.produkitem = cartitem.produk
        ulasan.save()
        return redirect(reverse("detail_transaksi_user_ulasan", kwargs={"id": id}))

    def get(self, request, id):
        cart = Cart.objects.get(pk=id)
        ulasan = UlasanCart.objects.filter(cart_id=id).first()
        data = {"cart": cart, "ulasan": ulasan, "range_value": range(1, 6)}
        return render(request, "profil/ulasan_transaksi.html", data)

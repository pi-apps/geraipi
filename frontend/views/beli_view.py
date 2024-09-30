from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from produk.models import Cart, CartItem
from profiles.models import UserProfileAddress

from .base_view import FrontPage


@method_decorator(login_required(login_url="/profile"), name="dispatch")
class Beli(FrontPage):
    def get(self, request, id):
        profile = request.user
        alamat = UserProfileAddress.objects.filter(userprofile_id=profile.pk, is_primary=True)
        alamat = alamat.first()
        # pajak = SettingWebsite.objects.filter(nama_pengaturan=3).first()
        pajak = self.configuration.pajak_beli
        pajak_persen = float(pajak) * 100
        cart_data = None
        try:
            cart = Cart.objects.get(user_id=request.user.id, status_pembayaran=1, pk=id)
            cart_data = CartItem.objects.filter(cart__user=request.user, cart__status_pembayaran=1).latest("pk")
            jumlah = 0
            harga = cart_data.jumlah * cart_data.produk.harga
            jumlah = jumlah + harga
            ppn = 0
            if jumlah > 0:
                ppn = float(pajak) * jumlah
            jumlah_ppn = jumlah + ppn
        except Exception as e:
            print(e)
            cart = None
            cart_data = None
            jumlah = 0
            ppn = 0
            jumlah_ppn = 0
        return render(
            request,
            "checkout/checkout_proses.html",
            {
                "cart": cart,
                "cart_item": cart_data,
                "jumlah": jumlah,
                "ppn": ppn,
                "jumlah_ppn": jumlah_ppn,
                "prosentase": pajak_persen,
                "alamat": alamat,
            },
        )

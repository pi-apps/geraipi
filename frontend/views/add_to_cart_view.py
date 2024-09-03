import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from produk.models import (
    AddressUserChartItem,
    Cart,
    CartItem,
    Produk,
    ProdukChartItem,
    StoreCartItem,
    UserCartItem,
)
from profiles.models import UserProfileAddress
from store.models import UserStore

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class AddToCart(FrontPage):
    def get(self, request, id):
        user = request.user
        if user.wallet is None:
            return redirect(reverse("profiles_edit"))
        useraddress = user.userprofileaddress_set.filter(is_primary=True).first()
        if not useraddress:
            return redirect(reverse("profile_detail"))
        produk = Produk.objects.get(pk=id)
        api_key = self.configuration.pajak_beli
        useraddress = request.user
        useraddress = useraddress.userprofileaddress_set.filter(is_primary=True).first()
        pajak_beli = float(api_key) * float(produk.harga)
        pajak_beli_total = pajak_beli + float(produk.harga)
        prosentase = float(api_key) * 100
        data = {
            "alamat": useraddress,
            "produk": produk,
            "jumlah_pajak": pajak_beli,
            "total_pajak": pajak_beli_total,
            "prosentase": prosentase,
        }
        return render(request, "checkout/home_beli.html", data)

    def post(self, request, id):
        produk = Produk.objects.get(pk=id)
        cart = Cart.objects.create(
            user=request.user,
            expedisi=request.POST.get("expedisi"),
            tanggal=datetime.datetime.now(),
            catatan=request.POST.get("catatan"),
        )
        cart.save()

        produk_cart = ProdukChartItem(
            store=produk.store,
            nama=produk.nama,
            harga=produk.harga,
            detail=produk.detail,
            stok_produk=produk.stok_produk,
            is_active=produk.is_active,
            stok=produk.stok,
            is_promo=produk.is_promo,
            berat=produk.berat,
            lebar=produk.lebar,
            slug=produk.slug,
            tipe=produk.tipe,
            created_at=produk.created_at,
        )
        produk_cart.save()
        produk_cart.kategori.set(produk.kategori.all())
        produk_cart.warna.set(produk.warna.all())

        user_cart = UserCartItem()
        user_cart.nama = request.user.nama
        user_cart.no_telepon = request.user.no_telepon
        user_cart.save()
        user_cart = UserCartItem.objects.get(pk=user_cart.id)

        addr_user = UserProfileAddress.objects.filter(
            userprofile_id=request.user.pk, is_primary=True
        ).first()
        user_cart_address = AddressUserChartItem()
        user_cart_address.address = addr_user.address
        user_cart_address.province = addr_user.province
        user_cart_address.distric = addr_user.distric
        user_cart_address.regency = addr_user.regency
        user_cart_address.village = addr_user.village
        user_cart_address.zipcode = addr_user.zipcode
        user_cart_address.userprofile = user_cart
        user_cart_address.typeaddress = addr_user.typeaddress
        user_cart_address.rt = addr_user.rt
        user_cart_address.rw = addr_user.rw
        user_cart_address.save()

        store_produk = UserStore.objects.filter(pk=produk.store.id).first()
        store_cart = StoreCartItem()
        store_cart.users = user_cart
        store_cart.nama = store_produk.nama
        store_cart.coin = store_produk.coin
        store_cart.deskripsi = store_produk.deskripsi
        store_cart.save()

        cart_item = CartItem.objects.create(
            cart=cart,
            produk=produk,
            produk_chart=produk_cart,
            user_chart=user_cart,
            store_chart=store_cart,
        )
        cart_item.save()

        return redirect(reverse("beli", kwargs={"id": cart.id}))

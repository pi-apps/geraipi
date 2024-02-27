from .base_view import FrontPage
from django.shortcuts import render
from produk.models import Produk
from store.models import UserStore

class Koleksi(FrontPage):
    def get(self, request, nama_toko):
        produk = Produk.objects.filter(store_id=nama_toko)
        store = UserStore.objects.get(id=nama_toko)
        return render(request, 'koleksi.html', {"store": store, "produk":produk})

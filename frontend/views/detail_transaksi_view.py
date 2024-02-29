from django.shortcuts import render

from frontend.views.base_view import FrontPage
from produk.models import Cart


class DetailTransaksi(FrontPage):
    def get(self, request):
        cart = Cart.objects.get(pk=request.GET.get("detail"))
        data = {"transaksi": cart}
        return render(request, "profil/transaksi_detail.html", data)

from django.shortcuts import render

from frontend.function_view.base_view import FrontPage
from produk.models import Produk


class Promo(FrontPage):
    def get(self, request):
        produk = Produk.objects.all()[:10]
        return render(request, "promo.html", {"produk": produk})

from produk.models import Kategori, Produk
from django.core.paginator import Paginator
from django.shortcuts import render
from .base_view import FrontPage


class SearchProduct(FrontPage):
    def get(self, request):
        kategori = Kategori.objects.all()
        produk = Produk.objects.filter(nama__icontains=request.GET.get('q', ""))
        pagination_produk = Paginator(produk, 25)
        pagination_produk = pagination_produk.get_page(request.GET.get("page", 1))
        return render(request, 'home/home_pencarian.html', {"produk": pagination_produk, "kategori": kategori})

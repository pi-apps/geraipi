from django.core.paginator import Paginator
from django.shortcuts import render

from produk.models import GambarProduk, Produk, UlasanCart
from profiles.models import LangSupport

from .base_view import FrontPage


class Detail(FrontPage):
    def get(self, request, slug):
        produk = Produk.objects.get(slug=slug)
        languages = LangSupport.objects.filter(is_active=True)
        gambar = None
        try:
            gambar = GambarProduk.objects.filter(produk_id=produk.id)
        except Exception as e:
            print(e)

        ulasan = UlasanCart.objects.filter(produkitem_id=produk.id)
        ulasan = Paginator(ulasan, 10)
        ulasan_page_num = request.GET.get("page", 1)
        ulasan = ulasan.page(ulasan_page_num)
        return render(
            request,
            "home/detail.html",
            {
                "slug": slug,
                "produk": produk,
                "gambar": gambar,
                "languages": languages,
                "ulasan": ulasan,
            },
        )

from django.core.paginator import Paginator
from django.shortcuts import render

from frontend.views.base_view import FrontPage
from produk.models import DeskripsiProduk, GambarProduk, Produk, UlasanCart
from profiles.models import LangSupport


class ProdukDetail(FrontPage):
    def get(self, request, slug):
        produk = Produk.objects.get(slug=slug)
        languages = LangSupport.objects.filter(is_active=True)
        gambar = None
        try:
            gambar = GambarProduk.objects.filter(produk_id=produk.id)
        except Exception as e:
            print(e)

        ulasan = UlasanCart.objects.filter(produkitem_id=produk.id).order_by(
            "-created_at"
        )
        ulasan = Paginator(ulasan, 10)
        ulasan_page_num = request.GET.get("page", 1)
        ulasan = ulasan.page(ulasan_page_num)
        user_lang = request.GET.get("language", None)
        if not user_lang:
            user_lang = DeskripsiProduk.objects.filter(produk__id=produk.id).first()
            user_lang = user_lang.languange.code
        try:
            deskripsi = DeskripsiProduk.objects.get(
                produk__id=produk.id, languange__code=user_lang
            )
        except Exception as e:
            deskripsi = {"deskripsi": f"{str(e)}"}
        return render(
            request,
            "produk/detail.html",
            {
                "slug": slug,
                "produk": produk,
                "deskripsi": deskripsi,
                "gambar": gambar,
                "languages": languages,
                "ulasan": ulasan,
                "deflang": user_lang,
            },
        )

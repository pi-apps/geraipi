from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render

from frontend.models import Pengumuman
from produk.models import Kategori, Produk

from .base_view import FrontPage


class Produks(FrontPage):
    def get(self, request):
        produk = Produk.objects.annotate(count_star=Avg("ulasancart__produk"))
        pengumuman = Pengumuman.objects.filter(is_active=True)
        pengumuman = pengumuman.first()

        kategori = None
        if request.GET.get("kategori"):
            kategori = Kategori.objects.filter(pk=request.GET.get("kategori")).first()
            produk = produk.filter(kategori__in=[request.GET.get("kategori")])
        produk_paginator = Paginator(produk, 100)
        page_number = request.GET.get("page")
        page_obj = produk_paginator.get_page(page_number)
        return render(
            request,
            "home/produk.html",
            {
                "produk": page_obj,
                "kategori": kategori,
                "range_value": range(1, 6),
                "pengumuman": pengumuman,
            },
        )

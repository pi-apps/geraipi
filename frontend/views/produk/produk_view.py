from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import render

from frontend.models import Pengumuman
from frontend.views.base_view import FrontPage
from produk.models import Kategori, Produk


class Produks(FrontPage):
    def get(self, request):
        produk = Produk.objects.annotate(
            count_star=Avg("ulasancart__produk"), terjual=Count("ulasancart__produk")
        ).order_by("?")
        pengumuman = Pengumuman.objects.filter(is_active=True)
        pengumuman = pengumuman.first()

        kategori = None
        if request.GET.get("kategori"):
            kategori = Kategori.objects.filter(pk=request.GET.get("kategori")).first()
            produk = produk.filter(kategori__in=[request.GET.get("kategori")])
        produk_paginator = Paginator(produk, 10)
        page_number = request.GET.get("page", 1)
        produk_page = produk_paginator.page(page_number)
        return render(
            request,
            "produk/produk.html",
            {
                "produk": produk_page,
                "produk_paginator": produk_paginator,
                "kategori": kategori,
                "range_value": range(1, 6),
                "pengumuman": pengumuman,
            },
        )

from django.shortcuts import render

from frontend.models import Pengumuman
from produk.models import Kategori
from master.models import Negara

from ..models import Banner
from .base_view import FrontPage


class Home(FrontPage):
    def get(self, request):
        # Pengumuman data
        pengumuman = Pengumuman.objects.filter(is_active=True)
        pengumuman = pengumuman.first()

        # Languange list
        languages = Negara.objects.all()

        kategori = []
        banner = Banner.objects.all()

        try:
            kategori = Kategori.objects.all()
        except Exception as e:
            print(e)
            kategori = []

        return render(
            request,
            "home/index.html",
            {
                "kategori": kategori,
                "banner": banner,
                "range_value": range(1, 6),
                "pengumuman": pengumuman,
                "languages": languages,
            },
        )

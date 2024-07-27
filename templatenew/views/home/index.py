from django.shortcuts import render

from frontend.models import Banner, Pengumuman
from master.models import Negara
from produk.models import Kategori
from templatenew.views.base_view import BaseView


class Home(BaseView):
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
            "home/page.html",
            {
                "kategori": kategori,
                "banner": banner,
                "range_value": range(1, 6),
                "pengumuman": pengumuman,
                "languages": languages,
            },
        )

from django.shortcuts import render

from frontend.views.base_view import FrontPage


class Tentang(FrontPage):
    def get(self, request):
        return render(request, "tentang.html", {})

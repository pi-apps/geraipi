from django.shortcuts import render

from frontend.views.base_view import FrontPage


class Faq(FrontPage):
    def get(self, request):
        return render(request, "faq.html")

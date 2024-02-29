from django.shortcuts import render

from frontend.views.base_view import FrontPage


class AboutApp(FrontPage):
    def get(self, request):
        return render(request, "aboutapps.html", {})

from django.shortcuts import render

from frontend.views.base_view import FrontPage


class TermOfService(FrontPage):
    def get(self, request):
        return render(request, "termofservice.html", {})

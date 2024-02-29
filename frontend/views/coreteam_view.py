from django.shortcuts import render

from frontend.views.base_view import FrontPage


class CoreTeam(FrontPage):
    def get(self, request):
        return render(request, "coreteam.html", {})

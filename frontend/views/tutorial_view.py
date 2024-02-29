from django.shortcuts import render

from frontend.function_view.base_view import FrontPage


class Tutorial(FrontPage):
    def get(self, request):
        return render(request, "tutorial.html", {})

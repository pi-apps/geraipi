from django.shortcuts import render

from frontend.function_view.base_view import FrontPage


class PrivacyAndPolicy(FrontPage):
    def get(self, request):
        return render(request, "privacyandpolicy.html", {})

from django.shortcuts import render

from frontend.views.base_view import FrontPage


class SocialMedia(FrontPage):
    def get(self, request):
        return render(request, "socialmedia.html", {})

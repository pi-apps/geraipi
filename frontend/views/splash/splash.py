from django.shortcuts import render

from frontend.views.base_view import FrontPage


class Splash(FrontPage):
    def get(self, request):
        return render(
            request,
            "splash/splash.html",
            {"file_splash": self.configuration.video_splash},
        )

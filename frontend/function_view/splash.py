from django.shortcuts import render
from .base_view import FrontPage

class Splash(FrontPage):
    def get(self, request):
        return render(request, 'splash.html',{})
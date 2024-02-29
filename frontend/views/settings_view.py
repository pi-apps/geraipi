from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from .base_view import FrontPage


@method_decorator(login_required(login_url="/profile"), name="dispatch")
class Settings(FrontPage):
    def get(self, request):
        return render(request, "setting.html")

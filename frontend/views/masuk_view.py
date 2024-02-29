from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .base_view import FrontPage


class Masuk(FrontPage):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            try:
                login(request, user)
            except Exception as e:
                print(e)
            return redirect("/home")

        else:
            return redirect("/masuk")

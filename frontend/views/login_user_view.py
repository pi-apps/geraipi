from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from profiles.models import UserProfile, UserSettingsMember

from .base_view import FrontPage


class LoginUser(FrontPage):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password", username)
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            usersetting = UserSettingsMember.objects.filter(user=user).first()
            if not usersetting:
                UserSettingsMember.objects.create(user=user)
            try:
                login(request, user)
                print("userss", user.is_authenticated)
            except Exception as e:
                print(e)
            return redirect("/home")
        else:
            user = UserProfile.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.set_password(password)
            user.save()
            usersetting = UserSettingsMember.objects.filter(user=user).first()
            if not usersetting:
                UserSettingsMember.objects.create(user=user)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/home")

    def get(self, request):
        username = request.GET.get("username")
        password = request.GET.get("password", username)
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            usersetting = UserSettingsMember.objects.filter(user=user).first()
            if not usersetting:
                UserSettingsMember.objects.create(user=user)
            try:
                login(request, user)
                print("userss", user.is_authenticated)
            except Exception as e:
                print(e)
            return redirect("/home")
        else:
            print("masuks")
            user = UserProfile.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.set_password(password)
            user.save()
            usersetting = UserSettingsMember.objects.filter(user=user).first()
            if not usersetting:
                UserSettingsMember.objects.create(user=user)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/home")

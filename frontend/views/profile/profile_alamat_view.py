from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from profiles.models import UserProfile, UserProfileAddress


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ProfileAlamat(FrontPage):
    def get(self, request):
        profile = request.user
        try:
            useraddress = UserProfileAddress.objects.filter(userprofile_id=profile.id)
        except UserProfileAddress.DoesNotExist:
            useraddress = None
        datas = {
            "address": useraddress,
        }
        return render(request, "profil/profile_alamat_.html", datas)

    def post(self, request):
        userss = request.user
        try:
            usernames = UserProfileAddress.objects.filter(userprofile_id=userss.id, pk=request.POST.get("id")).first()
            usernames.is_primary = True
            usernames.save()

            usernames = UserProfileAddress.objects.filter(userprofile_id=userss.id).exclude(pk=request.POST.get("id"))
            for a in usernames:
                a.is_primary = False
                a.save()

        except UserProfile.DoesNotExist:
            usernames = None
        return redirect(reverse("profile_detail"))

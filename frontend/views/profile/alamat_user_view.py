from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from profiles.models import UserProfileAddress

from ..base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class AlamatUser(FrontPage):
    def post(self, request):
        userprofile = request.user
        userdetail = UserProfileAddress()
        userdetail.address = request.POST.get("address", None)
        userdetail.zipcode = request.POST.get("zipcode", None)
        userdetail.rt = request.POST.get("rt", None)
        userdetail.rw = request.POST.get("rw", None)
        userdetail.province_id = request.POST.get("province", None)
        userdetail.regency_id = request.POST.get("regency", None)
        userdetail.distric_id = request.POST.get("distric", None)
        userdetail.userprofile_id = userprofile.pk
        userdetail.typeaddress = request.POST.get("origin")
        userdetail.save()
        return redirect(reverse("profile_detail"))

    def get(self, request):
        userprofile = request.user
        indo = True
        if userprofile.languages:
            if userprofile.languages.code != "id":
                indo = False

        userprofileaddress = UserProfileAddress.objects.filter(userprofile_id=request.user.id)
        return render(
            request,
            "profil/profile_alamat.html",
            {"address": userprofileaddress, "indo": indo},
        )

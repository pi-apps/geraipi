from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from store.models import UserStore, UserStoreAddress


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class AlamatToko(FrontPage):
    def get(self, request, id):
        userprofile = UserStore.objects.get(users_id=request.user.id)
        userprofileaddress = UserStoreAddress.objects.filter(userstore_id=userprofile.id)
        return render(request, "toko/alamat.html", {"address": userprofileaddress, "id": id})

    def post(self, request, id):
        userprofile = UserStore.objects.get(users_id=request.user.id)
        userprofileaddress = UserStoreAddress.objects.filter(userstore_id=userprofile.id)
        userprofileaddress = userprofileaddress.filter(pk=request.POST.get("id")).first()
        userprofileaddress.is_primary = True
        userprofileaddress.save()

        userprofileaddress = UserStoreAddress.objects.filter(userstore_id=userprofile.id)
        userprofileaddress = userprofileaddress.exclude(pk=request.POST.get("id"))
        for p in userprofileaddress:
            p.is_primary = False
            p.save()
        return redirect(reverse("alamat_toko", id))

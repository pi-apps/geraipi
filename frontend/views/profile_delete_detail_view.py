from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from profiles.models import UserProfileAddress

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class DeleteDetailProfile(FrontPage):
    def post(self, request, id_alamat):
        useralamat = UserProfileAddress.objects.get(pk=id_alamat)
        useralamat.delete()
        return redirect("/profile/alamat")

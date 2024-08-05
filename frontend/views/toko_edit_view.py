from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from store.models import UserStore

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
class TokoEdit(FrontPage):
    def get(self, request, id):
        usertoko = UserStore.objects.filter(users_id=id).first()
        return render(request, "toko/edit.html", {"user_toko": usertoko})

    def post(self, request, id):
        user = UserStore.objects.filter(users_id=id).first()
        if user is None:
            user = UserStore.objects.create(users_id=id)
        user.nama = request.POST.get("nama", "-")
        user.deskripsi = request.POST.get("deskripsi", "-")
        user.alamat = request.POST.get("alamat", "-")
        user.save()
        return redirect(reverse("toko", kwargs={"id": id}))

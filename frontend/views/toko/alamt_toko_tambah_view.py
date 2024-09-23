from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from store.models import UserStore, UserStoreAddress


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class AlamatTokoTambah(FrontPage):
    def get(self, request, id):
        local = True
        if request.GET.get("local"):
            local = False
        data = {"local": local, "toko_id": id}
        return render(request, "toko/alamat_tambah.html", data)

    def post(self, request):
        datas = request.POST
        stores = UserStore.objects.filter(users_id=id).first()
        alamat_toko = UserStoreAddress()
        alamat_toko.userstore = stores
        alamat_toko.province_id = datas.get("province")
        alamat_toko.regency_id = datas.get("regency")
        alamat_toko.distric_id = datas.get("distric")
        alamat_toko.rt = datas.get("rt")
        alamat_toko.rw = datas.get("rw")
        alamat_toko.zipcode = datas.get("zipcode")
        alamat_toko.address = datas.get("address")
        alamat_toko.save()
        return redirect(reverse("alamat_toko", id))

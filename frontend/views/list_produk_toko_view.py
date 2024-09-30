from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from produk.models import Produk
from store.models import UserStore

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ListProdukToko(FrontPage):
    def get(self, request, id):
        produk = Produk.objects.filter(store__users_id=request.user.id, is_archive=False)
        store = UserStore.objects.filter(pk=id)
        data = {"produk": produk, "store": store}
        return render(request, "toko/listproduk.html", data)

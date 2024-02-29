from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.function_view.base_view import FrontPage
from produk.models import Produk


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class ArchiveBarang(FrontPage):
    def post(self, request, id, produk_id):
        produk = Produk.objects.get(pk=produk_id)
        produk.is_archive = True
        produk.save()
        return redirect(reverse("list_produk_toko", str(id)))

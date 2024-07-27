from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from master.models import Country
from produk.models import (
    DeskripsiProduk,
    Expedisi,
    GambarProduk,
    Kategori,
    Produk,
    TipeProduk,
    WarnaProduk,
)
from profiles.models import LangSupport
from store.models import UserStore

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class Jual(FrontPage):
    def get(self, request):
        user = UserStore.objects.filter(users_id=request.user.id)
        if user.exists():
            user = user.first()
            if user.is_active_store is False:
                return redirect(reverse("profile"))
        else:
            return redirect(reverse("profile"))
        kategori = Kategori.objects.all()
        typeproduk = TipeProduk.objects.all()
        warnaproduk = WarnaProduk.objects.all()
        expedisi = Expedisi.objects.all()
        languages = LangSupport.objects.filter(is_active=True)
        country = Country.objects.filter(is_active=True)
        return render(
            request,
            "jual/index.html",
            {
                "kategori": kategori,
                "typeproduk": typeproduk,
                "warnaproduk": warnaproduk,
                "ekspedisi": expedisi,
                "languages": languages,
                "country": country,
            },
        )

    def post(self, request):
        refinput = request.POST
        reffile = request.FILES
        store = None
        try:
            store = UserStore.objects.get(users__pk=request.user.id)
        except Exception:
            store = UserStore.objects.create(
                users=request.user, nama=request.user.username
            )
            messages.error(request, "Belum Mempunyai Toko")
            return redirect(reverse("jual"))

        produk = Produk.objects.filter(
            store__id=store.id, nama=refinput.get("nama", "")
        ).first()
        if produk:
            messages.error(request, "Produk sudah ada")
            return redirect(reverse("jual"))

        produk = Produk.objects.create(
            store=store,
            nama=refinput.get("nama", ""),
            harga=refinput.get("harga", 1),
            detail=refinput.get("deskripsi", "-"),
            stok_produk=refinput.get("stok", 1),
            berat=refinput.get("berat"),
            lebar=refinput.get("lebar"),
            cross_boarder=refinput.get("lintas_negara", False),
            negara_id=refinput.get("negara", None),
            tipe_id=refinput.get("tipe"),
        )
        for k in refinput.getlist("kategori"):
            kateg = Kategori.objects.filter(pk=k).first()
            produk.kategori.add(kateg)

        for k in refinput.getlist("warna"):
            try:
                warnaa = WarnaProduk.objects.filter(pk=k).first()
            except Exception as e:
                print(e)
                warnaa = WarnaProduk.objects.filter(nama=k).first()
            if warnaa:
                produk.warna.add(warnaa)
            else:
                warnaa = WarnaProduk.objects.create(nama=k)
                produk.warna.add(warnaa)
        lang = LangSupport.objects.get(code=refinput.get("bahasa", "id"))
        input_data = refinput.get("deskripsi|" + lang.code)
        DeskripsiProduk.objects.create(
            produk=produk, languange=lang, deskripsi=input_data
        )

        for reffiles in reffile.getlist("gambar"):
            GambarProduk.objects.create(
                produk=produk, nama=refinput.get("nama", "-"), gambar=reffiles
            )
        messages.success(request, "Produk Berhasil disimpan")
        return redirect(reverse("jual"))

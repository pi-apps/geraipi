from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from produk.models import GambarProduk, Kategori, Produk, TipeProduk, WarnaProduk


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class EditBarang(FrontPage):
    def get(self, request, id, produk_id):
        produk = Produk.objects.filter(pk=produk_id).first()
        image = {"gambar1": None, "gambar2": None, "gambar3": None}
        if produk.gambarproduk_set:
            produks_image = produk.gambarproduk_set.all()
            gambar_number = 1
            for gambar in produks_image:
                image.update({"gambar" + str(gambar_number): gambar.gambar})
                gambar_number += 1
        kategori = Kategori.objects.all()
        tipe = TipeProduk.objects.all()
        warna = WarnaProduk.objects.all()
        data = {
            "data": produk,
            "images": image,
            "kategori": kategori,
            "typeproduk": tipe,
            "warnaproduk": warna,
        }
        return render(request, "toko/edit_barang.html", data)

    def post(self, request, id, produk_id):
        produk = Produk.objects.filter(pk=produk_id).first()
        image = {"gambar1": None, "gambar2": None, "gambar3": None}
        if produk.gambarproduk_set:
            produks_image = produk.gambarproduk_set.all()
            gambar_number = 1
            for gambar in produks_image:
                image.update({"gambar" + str(gambar_number): gambar.gambar})
                gambar_number += 1

        nama = request.POST.get("nama")
        deskripsi = request.POST.get("deskripsi")
        stok = request.POST.get("stok")
        harga = request.POST.get("harga")
        kategori_post = request.POST.getlist("kategori")
        tipe_post = request.POST.get("tipe")
        warna_post = request.POST.getlist("warna")
        berat = request.POST.get("berat")
        lebar = request.POST.get("lebar")

        produk.nama = nama
        produk.detail = deskripsi
        produk.stok_produk = stok
        produk.harga = harga
        produk.berat = berat
        produk.lebar = lebar
        produk.cross_boarder = (
            True if request.POST.get("cross_boarder", None) else False
        )
        produk.tipe_id = tipe_post
        produk.save()

        produk.kategori.remove()
        produk.warna.remove()

        for k in kategori_post:
            kateg = Kategori.objects.filter(pk=k).first()
            produk.kategori.add(kateg)

        for k in warna_post:
            # warna = None
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

        filess1 = request.FILES.get("gambar1")
        filess2 = request.FILES.get("gambar2")
        filess3 = request.FILES.get("gambar3")

        if filess1:
            gproduk = GambarProduk.objects.filter(
                sortings=1, produk_id=produk.pk
            ).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=1, produk=produk, nama=nama, gambar=filess1
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess1
                gproduk.save()

        if filess2:
            gproduk = GambarProduk.objects.filter(
                sortings=2, produk_id=produk.pk
            ).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=2, produk=produk, nama=nama, gambar=filess2
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess2
                gproduk.save()

        if filess3:
            gproduk = GambarProduk.objects.filter(
                sortings=3, produk_id=produk.pk
            ).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=3, produk=produk, nama=nama, gambar=filess3
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess3
                gproduk.save()
        return redirect(reverse("list_produk_toko", kwargs={"id": str(id)}))

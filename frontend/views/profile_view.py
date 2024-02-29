from django.shortcuts import render

from produk.models import Cart

from .base_view import FrontPage


class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        try:
            pesanan = {
                "pesanan": Cart.objects.filter(
                    status=2, status_toko=1, user=request.user.id
                ).count(),
                "diproses": Cart.objects.filter(
                    status=2, status_toko=2, user=request.user.id
                ).count(),
                "dikirim": Cart.objects.filter(
                    status=2, status_toko=3, user=request.user.id
                ).count(),
            }
        except Exception as e:
            print(e)
            pesanan = {"pesanan": 0, "diproses": 0, "dikirim": 0}
        datas = {"status_pesanan": pesanan, "profile": profile}
        return render(request, "profil/profile.html", datas)

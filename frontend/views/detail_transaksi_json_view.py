from django.http import JsonResponse

from frontend.function_view.base_view import FrontPage
from produk.models import CartItem


class DetailTransaksiJson(FrontPage):
    def get(self, request):
        cartitem = CartItem.objects.filter(pk=request.GET.get("detail", 0)).first()
        data = {
            "success": True,
            "data": {
                "cart": cartitem.cart.kode,
                "tanggal": cartitem.cart.tanggal.date(),
                "jumlah": cartitem.jumlah,
                "resi": cartitem.cart.nomor_resi,
                "produk": {
                    "nama_produk": cartitem.produk.nama,
                    "harga": cartitem.produk_chart.harga,
                },
            },
        }
        return JsonResponse(data)

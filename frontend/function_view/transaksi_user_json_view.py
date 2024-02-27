from django.http import JsonResponse

from produk.models import CartItem

from .base_view import FrontPage


class TransaksiUserJson(FrontPage):
    def get(self, request):
        data = {"success": False}
        try:
            transaksi = CartItem.objects.filter(
                cart__user_id=request.user.id, cart__status=request.GET.get("status", 1)
            )
            data.update(
                {
                    "success": True,
                    "data": [
                        {
                            "id": x.id,
                            "nama_barang": x.produk.nama or "-",
                            "tanggal": x.cart.tanggal.date() if x.cart.tanggal else "",
                            "resi": x.cart.nomor_resi,
                        }
                        for x in transaksi
                    ],
                }
            )
        except Exception as e:
            print(e)
            data.update({"data": []})
        return JsonResponse(data)

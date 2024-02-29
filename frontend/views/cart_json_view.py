from django.http import JsonResponse

from frontend.views.base_view import FrontPage
from produk.models import CartItem


class CartJson(FrontPage):
    def get(self, request, id):
        cartitem = CartItem.objects.filter(pk=id).first()
        # pajak = SettingWebsite.objects.filter(nama_pengaturan=3).first()
        pajak = float(self.configuration.pajak_beli)
        # pajak_persen = float(pajak) * 100
        data = {"success": False}
        if cartitem:
            barang_harga = cartitem.produk.harga
            barang_jumlah = cartitem.jumlah
            barang_total = barang_harga * barang_jumlah
            barang_pajak = barang_total * pajak
            harga_total = barang_total + barang_pajak
            data = {
                "success": True,
                "harga_total": harga_total,
                "barang_total": barang_total,
            }
        return JsonResponse(data)

import requests
from django.http import JsonResponse

from frontend.function_view.base_view import FrontPage
from produk.models import Cart
from projekpi.pi_network import PiNetwork


class SetComplete(FrontPage):
    def completepayment(self, request, id):
        api_key = self.configuration.api_key_pi
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        pi.complete_payment(id)

    def get(self, request, id):
        api_key = self.configuration.api_key_pi
        datas = {"txid": request.GET.get("txid")}
        postdata = requests.post(
            "https://api.minepi.com/v2/payments/" + id + "/complete",
            data=datas,
            headers={"Authorization": "Key " + api_key},
            timeout=5000,
        )
        if postdata.status_code == 200:
            cart = Cart.objects.get(pk=request.GET.get("id"))
            cart.status = 2
            cart.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False})

import requests
from django.http import JsonResponse

from frontend.views.base_view import FrontPage
from projekpi.pi_network import PiNetwork


class Cancel(FrontPage):
    def get(self, request, id):
        api_key = self.configuration.api_key_pi
        wallet_private_seed = self.configuration.wallet_private_pi
        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        cancel = requests.get(
            "https://api.minepi.com/payments/" + id + "/cancel",
            headers={"Authorization": "Key " + api_key},
            timeout=5000,
        )
        print(cancel.json())
        return JsonResponse(cancel, safe=False)

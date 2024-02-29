from django.http import JsonResponse

from frontend.function_view.base_view import FrontPage
from projekpi.pi_network import PiNetwork


class PaymentCartCancel(FrontPage):
    def get(self, request, param_id):
        api_key = self.configuration.api_key_pi
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        cancel = pi.cancel_payment_user(param_id)
        return JsonResponse(cancel, safe=False)

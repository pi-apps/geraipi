from frontend.views.base_view import FrontPage
from projekpi.pi_network import PiNetwork


class CompletePayment(FrontPage):
    def get(self, request, id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        pi.complete_payment(id)

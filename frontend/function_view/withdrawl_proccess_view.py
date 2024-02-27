from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from master.models import HistoriTampung
from profiles.models import UserWithdrawlTransaction
from projekpi.pi_network import PiNetwork

from .base_view import FrontPage


class WithdrawlProcess(FrontPage):
    def get(self, request):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi

        # pajak_widtdrawl = SettingWebsite.objects.filter(nama_pengaturan=4).first()
        pajak_widtdrawl = self.configuration.pajak_withdrawl

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)

        user_uid = request.GET.get("user_id")
        jumlah = request.GET.get("jumlah")
        if jumlah:
            try:
                if float(jumlah) >= 0.0:
                    jumlah = float(jumlah)
                    payment_data = {
                        "amount": jumlah,
                        "memo": "Pembayaran - Greetings from Geraipi",
                        "metadata": {"product_id": "apple-pie-1"},
                        "uid": user_uid,
                    }
                    payment_id = pi.create_payment(payment_data)
                    txid = pi.submit_payment(payment_id, False)
                    payment = pi.complete_payment(payment_id, txid)

                    transaction = UserWithdrawlTransaction.objects.create(
                        user=request.user, jumlah=jumlah
                    )

                    pajaks = HistoriTampung(jumlah=jumlah)
                    pajaks.save()

                    userprofile = request.user
                    userprofile.coin = float(userprofile.coin) - float(jumlah)
                    userprofile.save()

                    return JsonResponse({"success": True}, safe=False)
                else:
                    print("error masuk", float(jumlah))
                    return JsonResponse({"success": False}, safe=False)
            except Exception as e:
                print(e)
        return JsonResponse({"success": False}, safe=False)

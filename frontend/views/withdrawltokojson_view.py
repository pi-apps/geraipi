from django.http import JsonResponse

from frontend.function_view.base_view import FrontPage
from store.models import UserStore, UserStoreWdHistory


class WithdrawlTokoJson(FrontPage):
    def get(self, request, id):
        toko = UserStore.objects.get(users_id=id)
        user = request.user
        from firebase_admin import messaging

        jumlah = request.GET.get("jumlah", 0)
        if jumlah:
            if float(jumlah) > 0 and float(toko.coin) > 0:
                pajak = self.configuration.pajak_withdrawl
                jumlah_pajak = float(jumlah) - (pajak * float(jumlah))
                toko.coin = float(toko.coin) - float(jumlah)
                user.coin = float(user.coin) + float(jumlah_pajak)
                toko.save()
                user.save()

                self.configuration.koin_website = pajak
                self.configuration.save()

                userwd = UserStoreWdHistory()
                userwd.jumlah = jumlah_pajak
                userwd.userstore = toko
                userwd.save()
                if user.fcm_token:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="notification",
                            body="test notification",
                        ),
                        token=str(user.fcm_token),
                    )
                    messa = messaging.send(message)
                    print(type(user.fcm_token), messa)

                return JsonResponse({"success": True})
        return JsonResponse({"success": False})

from django.http import JsonResponse

from frontend.views.base_view import FrontPage
from profiles.models import UserSettingsMember
from store.models import UserStore, UserStoreWdHistory


class WithdrawlTokoJson(FrontPage):
    def get(self, request, id):
        usersetting = UserSettingsMember.objects.get(user_id=request.user.id)
        toko = UserStore.objects.get(users_id=id)
        user = request.user
        from firebase_admin import messaging

        jumlah = request.GET.get("jumlah", 0)
        if jumlah:
            if float(jumlah) > 0 and float(toko.coin) > 0:
                pajak = usersetting.tier.pajak_withdrawl
                if usersetting.tier.kuota_withdrawl > 0:
                    pajak = 0
                    if usersetting.kuota >= usersetting.tier.kuota_withdrawl:
                        pajak = usersetting.tier.pajak_withdrawl
                # pajak = self.configuration.pajak_withdrawl
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
                if usersetting.tier.kuota_withdrawl > 0:
                    if usersetting.kuota < usersetting.tier.kuota_withdrawl:
                        usersetting.kuota = usersetting.kuota + 1
                        usersetting.save()
                if user.fcm_token:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="Withdrawl",
                            body="User telah withdraw",
                        ),
                        token=str(user.fcm_token),
                    )
                    messaging.send(message)

                return JsonResponse({"success": True})
        return JsonResponse({"success": False})

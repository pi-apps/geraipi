import requests
from django.http import JsonResponse
from firebase_admin import messaging

from frontend.views.base_view import FrontPage


class Approve(FrontPage):
    def get(self, request, id):
        # settingweb = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        print(self.configuration.api_key_pi)
        settingweb = self.configuration.api_key_pi
        header = {"Authorization": "Key " + settingweb}
        postdata = requests.post(
            "https://api.minepi.com/v2/payments/" + id + "/approve",
            headers=header,
            timeout=500000,
        )
        if postdata.status_code == 200:
            try:
                if request.user.fcm_token:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="Produk",
                            body="User telah menambahkan produk",
                        ),
                        token=str(request.user.fcm_token),
                    )
                    messaging.send(message)
            except Exception as e:
                print(str(e))
            return JsonResponse(postdata.json())
        else:
            return JsonResponse({"status": False, "message": postdata.json()})

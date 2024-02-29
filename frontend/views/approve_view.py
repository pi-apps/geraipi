import requests
from django.http import JsonResponse

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
            timeout=5000,
        )
        if postdata.status_code == 200:
            return JsonResponse(postdata.json())
        else:
            return JsonResponse({"status": False, "message": postdata.json()})

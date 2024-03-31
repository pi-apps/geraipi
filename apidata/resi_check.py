import requests


class ResiCheck:
    def __init__(self, url, api):
        self.url = url
        self.api = api

    def check_resi(self, resi, courier):
        try:
            header = {
                "key": self.api
            }
            payload = {
                "waybill": resi,
                "courier": courier
            }
            response = requests.post(url=self.url, headers=header, data=payload)
            return response
        except Exception as e:
            return e

    def check_resi_bitesip(self, resi, courier):
        try:
            # 
            header = {
                "authorization": self.api
            }
            url = f"https://api.biteship.com/v1/trackings/{resi}/couriers/{courier}"
            response = requests.get(url=url, headers=header)
            return response
        except Exception as e:
            return e

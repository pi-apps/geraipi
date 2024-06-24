import json

import requests

# from django.core.mail import EmailMessage
from django.http import JsonResponse

from frontend.views.base_view import FrontPage
from produk.models import Cart, CartItem, Produk
from store.models import UserStore

# from django.template.loader import render_to_string


class PaymentsCart(FrontPage):
    def setcomplete(self, request, cart_id, identifier, param):
        api_key = self.configuration.api_key_pi
        datas = {"txid": param}
        try:
            postdata = requests.post(
                "https://api.minepi.com/v2/payments/" + identifier + "/complete",
                data=datas,
                headers={"Authorization": "Key " + api_key},
                timeout=500000,
            )

            if postdata.status_code == 200:
                print(postdata, cart_id, identifier)
                cart = Cart.objects.get(pk=cart_id)
                cart.status_toko = 1
                cart.status_pembayaran = 2
                cart.save()

                cartitem = CartItem.objects.get(cart__id=cart.id)
                produk = Produk.objects.get(pk=cartitem.produk.id)
                produk.stok_produk = produk.stok_produk - 1
                produk.save()

                users = UserStore.objects.get(pk=produk.store.pk)
                # users.coin += produk.harga * cartitem.jumlah
                users.save()
                return {"status": True}
            else:
                return {"status": False}
        except Exception as e:
            print(e)
            return {"status": False}

    def get(self, request, param):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        data_url = "https://api.minepi.com/v2/payments/" + param
        requestdata = requests.get(
            data_url, headers={"Authorization": "Key " + api_key}, timeout=500000
        )

        cart_id = request.GET.get("cart_id")
        requestjson = requestdata.json()
        result_dict = json.loads(str(json.dumps(requestjson)))
        # try:
        #     carts = CartItem.objects.get(pk=cart_id)
        #     print(carts, cart_id)
        #     CartItem.objects.get(cart__id=carts.id)
        #     from django.core.mail import EmailMessage
        #     from django.template.loader import render_to_string

        #     # print(carts, cartitems)
        #     subject, from_email, to = (
        #         "Payment Success GeraiPi",
        #         "payment@geraipi.com",
        #         request.user.email,
        #     )
        #     html_message = render_to_string("mail_template.html", {"carts": carts})
        #     # # plain_message = strip_tags(html_message)
        #     # # mail.send_mail(subject,
        #     # #     plain_message,
        #     # #     from_email,
        #     # #     [to],
        #     # #     html_message=html_message)

        #     msg = EmailMessage(subject, html_message, from_email, [to])
        #     msg.content_subtype = "html"
        #     msg.send()

        # except CartItem.DoesNotExist or Exception as e:
        #     print("error")

        txid = result_dict.get("transaction")
        txid = json.loads(str(json.dumps(txid)))
        txid = txid.get("txid")
        t = self.setcomplete(request, cart_id, param, txid)
        return JsonResponse(t, safe=False)

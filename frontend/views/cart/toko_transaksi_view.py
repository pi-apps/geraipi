import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import messaging

from frontend.views.base_view import FrontPage
from produk.models import Cart, CartItem
from store.models import Expedisi, UserStore


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required(login_url="/profile"), name="dispatch")
class TransaksiToko(FrontPage):
    def post(self, request, id):
        status = request.GET.get("status", 1)
        status_posisi = "diambil"
        if status:
            cart = Cart.objects.get(pk=request.POST.get("cart_id"))
            if cart.status_toko == 1:
                cart.status_toko = 2
                cart.status = 2
            elif cart.status_toko == 2:
                resi = request.POST.get("nomor_resi").strip()
                layanan = request.POST.get("expedisi").strip()
                if resi and layanan:
                    cart.nomor_resi = resi
                    cart.tanggal_dikirim = datetime.datetime.now()
                    cart.status_toko = 3
                    cart.status = 3
                    cart.expedisi_id = request.POST.get("expedisi")
                    cek = Cart.objects.filter(nomor_resi=resi)
                    if cek.exists():
                        messages.error(request, "Sorry, Nomor resi sudah digunakan")
                        urls_redirect = reverse(
                            "transaksi_toko",
                            kwargs={"id": str(request.user.id)},
                        )
                        return redirect(f"{urls_redirect}?status={str(status)}")
                    from apidata.resi_check import ResiCheck
                    from master.models import ConfigurationWebsite

                    konfigurasi = ConfigurationWebsite.get_solo()
                    cekinit = ResiCheck(
                        url=konfigurasi.url_check_resi, api=konfigurasi.api_check_resi
                    )
                    code_expedisi = Expedisi.objects.get(
                        id=request.POST.get("expedisi")
                    )
                    status_posisi = "dikirim"
                    if not konfigurasi.bypass_expedisi:
                        if code_expedisi.source_request == 1:
                            cekresi = cekinit.check_resi(
                                resi=resi, courier=code_expedisi.code
                            )
                            if cekresi.status_code != 200:
                                url_redirect = reverse(
                                    "transaksi_toko",
                                    kwargs={"id": str(request.user.id)},
                                )
                                return redirect(f"{url_redirect}?status={str(status)}")
                            else:
                                messages.success(request, "Nomor resi valid")
                                cart.save()
                                url_redirect = reverse(
                                    "transaksi_toko",
                                    kwargs={"id": str(request.user.id)},
                                )
                                return redirect(f"{url_redirect}?status={str(status)}")
                        elif code_expedisi.source_request == 2:
                            cekinit.api = konfigurasi.api_biteship
                            cekresi = cekinit.check_resi_bitesip(
                                resi=resi, courier=code_expedisi.code
                            )
                            if cekresi.status_code != 200:
                                cart.save()
                                messages.success(request, "Nomor resi valid")
                                url_redirect = reverse(
                                    "transaksi_toko",
                                    kwargs={"id": str(request.user.id)},
                                )
                                return redirect(f"{url_redirect}?status={str(status)}")
                            else:
                                messages.error(request, "Sorry, Nomor resi tidak valid")
                                url_redirect = reverse(
                                    "transaksi_toko",
                                    kwargs={"id": str(request.user.id)},
                                )
                                return redirect(f"{url_redirect}?status={str(status)}")
                    else:
                        cart.save()
                        messages.success(request, "Nomor resi valid")
                        url_redirect = reverse(
                            "transaksi_toko",
                            kwargs={"id": str(request.user.id)},
                        )
                        return redirect(f"{url_redirect}?status={str(status)}")
                else:
                    messages.error(request, "Sorry, please input your number")

                    url_redirect = reverse(
                        "transaksi_toko",
                        kwargs={"id": str(request.user.id)},
                    )
                    return redirect(f"{url_redirect}?status={str(status)}")
            elif cart.status_toko == 3:
                cart.status = 3
                cart.tanggal_selesai = datetime.datetime.now()
                # cart.status_toko = 4
                status_posisi = "selesai"
            try:
                self.send_mail(request)
            except Exception as e:
                print(e)
            try:
                if request.user.fcm_token:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title="Transaksi",
                            body=f"User telah {status_posisi} pesanan",
                        ),
                        token=str(request.user.fcm_token),
                    )
                    messaging.send(message)
            except Exception as e:
                print(str(e))
            cart.save()
        return redirect("/toko/" + str(request.user.id) + "/transaksi/")

    def send_mail(self, request):
        from smtplib import SMTPException

        from django.core.mail import EmailMessage, get_connection
        from django.template.loader import render_to_string

        # print(carts, cartitems)
        try:
            with get_connection(
                host=self.email_host,
                port=self.email_port,
                username=self.email_user,
                password=self.email_password,
                use_ssl=True,
                use_tls=False,
            ) as connection:
                subject = "Payment Success GeraiPi"
                from_email = "Admin <{}>".format("admin@geraipi.id")
                html = render_to_string("mail_template.html")
                to = [
                    request.user.email,
                ]
                sendd = EmailMessage(
                    subject, html, from_email, to, connection=connection
                )
                sendd.content_subtype = "html"
                sendd.send()
        except SMTPException as e:
            print(request.user.email)
            print("Email => ", str(e))

    # def send_telegram(self, message):
    #     from projekpi.telegram_utils import TelegramService

    #     telegram = TelegramService(
    #         "+6281556776939", "Roni", "890218", ""
    #     )
    #     telegram.connection()
    #     telegram.initial_auth()

    def get(self, request, id):
        expedisi = Expedisi.objects.all()
        context = {
            "produk": None,
            "expedisi": expedisi,
            "pesanan": 0,
            "diproses": 0,
            "dikirim": 0,
        }
        status = request.GET.get("status", 1)
        store = UserStore.objects.get(users_id=request.user.id)
        if status:
            produk = CartItem.objects.filter(
                # cart__user_id=request.user.id,
                cart__status_toko=status,
                produk__store_id=store.id,
                cart__status_pembayaran=2,
            )
            context.update({"produk": produk})
        context.update(
            {
                "pesanan": CartItem.objects.filter(
                    cart__status_toko=1,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
                "diproses": CartItem.objects.filter(
                    cart__status_toko=2,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
                "dikirim": CartItem.objects.filter(
                    cart__status_toko=3,
                    produk__store_id=store.id,
                    cart__status_pembayaran=2,
                ).count(),
            }
        )
        return render(request, "toko/listtransaksi.html", context)

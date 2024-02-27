import calendar
import datetime
import json
import time
import os
from typing import Any
from django.http.response import HttpResponse as HttpResponse
# from passkeys.models import UserPasskey


import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.mail import EmailMessage, get_connection
from django.core.paginator import Paginator
from django.core.signals import request_finished
from django.db.models import Avg, OuterRef, Q, Subquery
from django.dispatch import receiver
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from frontend.models import Banner
from master.models import ConfigurationWebsite, HistoriTampung, SettingWebsite
from produk.models import (AddressUserChartItem, Cart, CartItem, GambarProduk,
                           Kategori, Produk, ProdukChartItem,
                           StoreAddressCartItem, StoreCartItem, TipeProduk,
                           UlasanCart, UserCartItem, WarnaProduk)
from profiles.models import (UserProfile, UserProfileAddress,
                             UserWithdrawlTransaction)
from projekpi.pi_network import PiNetwork
from store.models import UserStore, UserStoreAddress, UserStoreWdHistory, Expedisi

from .function_view.base_view import FrontPage

@method_decorator(csrf_exempt, name='dispatch')
class UploadDropzone(FrontPage):
    def get(self, request):
        return JsonResponse({ "status":True, "uuid":"1" })
    
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class Jual(FrontPage):
    def get(self, request):
        user = UserStore.objects.filter(users_id=request.user.id)
        if user.exists():
            user = user.first()
            if user.is_active_store is False:
                return redirect('/profile')
        kategori = Kategori.objects.all()
        typeproduk = TipeProduk.objects.all()
        warnaproduk = WarnaProduk.objects.all()
        expedisi = Expedisi.objects.all()
        return render(request, 'jualpage.html',{
            "kategori": kategori,
            "typeproduk": typeproduk,
            "warnaproduk": warnaproduk,
            "ekspedisi": expedisi
        })
    
    def post(self, request):
        refinput = request.POST
        reffile = request.FILES
        store = None
        try:
            store = UserStore.objects.get(users__pk=request.user.id)
        except Exception as e:
            store = UserStore.objects.create(users=request.user, nama=request.user.username)
        
        try:
            produk = Produk.objects.get(store__id=store.id, nama=refinput.get('nama',''))
            messages.error(request, "Produk sudah ada")
        except Exception as e:
            produk = Produk.objects.create(
                store=store, 
                nama=refinput.get('nama',''), 
                harga=refinput.get("harga",1), 
                detail=refinput.get("deskripsi","-"), 
                stok_produk=refinput.get("stok",1),
                berat=refinput.get("berat"),
                lebar=refinput.get("lebar"),
                cross_boarder=refinput.get("lintas_negara", False)
            )
            for k in refinput.getlist("kategori"):
                kateg = Kategori.objects.filter(pk=k).first()
                produk.kategori.add(kateg)

            for k in refinput.getlist("warna"):
                warna = None
                try:
                    warnaa = WarnaProduk.objects.filter(pk=k).first()
                except Exception as e:
                    warnaa = WarnaProduk.objects.filter(nama=k).first()
                if warnaa:
                    produk.warna.add(warnaa)
                else:
                    warnaa = WarnaProduk.objects.create(nama=k)
                    produk.warna.add(warnaa)

            tipes = TipeProduk.objects.filter(pk=refinput.get('tipe')).first()
            produk.tipe.add(tipes)
            # print(reffile.get("gambar"))
            for reffiles in reffile.getlist("gambar"):
                gambarproduk = GambarProduk.objects.create(
                    produk=produk, 
                    nama=refinput.get("nama","-"), 
                    gambar=reffiles
                )
        messages.success(request, "Produk Berhasil disimpan")
        return redirect("/jual/")

@method_decorator(csrf_exempt, name='dispatch')
class DetailProfileAddressMain(FrontPage):
    def post(self, request, id):
        userss = UserProfile.objects.get(users_id=request.user.id)
        data = {"status": False}
        try:
            usernames = UserProfileAddress.objects.get(userprofile_id=userss.pk, pk=id)
            usernames.is_primary = True 
            usernames.save()
            useraddress2 = UserProfileAddress.objects.filter(userprofile_id=userss.pk).exclude(id=id)
            for useraddresss in useraddress2:
                useraddresss.is_primary = False
                useraddresss.save()
            data = {
                "status": True
            }
        except UserProfile.DoesNotExist:
            data = {
                "status": False
            }
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class AlamatToko(FrontPage):
    def get(self, request, id):
        userprofile = UserStore.objects.get(users_id=request.user.id)
        userprofileaddress = UserStoreAddress.objects.filter(userstore_id=userprofile.id)
        return render(request, 'toko/alamat.html', {"address": userprofileaddress, "id": id})
    
    def post(self, request, id):
        userprofileaddress = userprofileaddress.filter(pk=request.POST.get('id')).first()
        userprofileaddress.is_primary = True
        userprofileaddress.save()

        userprofileaddress = UserStoreAddress.objects.filter(userstore_id=userprofile.id)
        userprofileaddress = userprofileaddress.exclude(pk=request.POST.get('id'))
        for p in userprofileaddress:
            p.is_primary = False
            p.save()
        return redirect('/toko/{}/alamat'.format(id))

@method_decorator(csrf_exempt, name='dispatch')
class DeleteAlamatToko(FrontPage):
    def post(self, request, id, id_alamat):
        userprofileaddress = UserStoreAddress.objects.get(pk=id_alamat)
        userprofileaddress.delete()
        return redirect('/toko/{}/alamat'.format(id))


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class AlamatTokoTambah(FrontPage):
    def get(self, request, id):
        local = True
        if request.GET.get("local"):
            local=False
        data = {
            "local": local,
            "toko_id": id
        }
        return render(request, 'toko/alamat_tambah.html', data)
    def post(self, request):
        datas = request.POST
        stores = UserStore.objects.filter(users_id=id).first()
        alamat_toko = UserStoreAddress()
        alamat_toko.userstore = stores
        alamat_toko.province_id = datas.get('province')
        alamat_toko.regency_id = datas.get('regency')
        alamat_toko.distric_id = datas.get('distric')
        alamat_toko.rt = datas.get('rt')
        alamat_toko.rw = datas.get('rw')
        alamat_toko.zipcode = datas.get('zipcode')
        alamat_toko.address = datas.get('address')
        alamat_toko.save()
        return redirect('/toko/{}/alamat'.format(id))
        

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class AddToCartAppend(FrontPage):
    def get(self, request, id):
        produk = Produk.objects.get(pk=id)
        cart = Cart.objects.filter(user=request.user.id, status=1)
        cart = cart.first()
        if not cart:
            cart = Cart.objects.create(
                user = request.user,
                status=1
            )
            cart.save()

        cart_item = CartItem.objects.create(
            cart=cart,
            produk=produk
        )
        cart_item.save()
        return JsonResponse({'status':True})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class AddToCart(FrontPage):
    def get(self, request, id):
        user = request.user
        if user.wallet is None:
            return redirect(reverse('profiles_edit'))
        useraddress = user.userprofileaddress_set.filter(is_primary=True).first()
        if not useraddress:
            return redirect(reverse("profile_detail"))
        produk = Produk.objects.get(pk=id)
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=3).first()
        api_key = self.configuration.pajak_beli
        useraddress = request.user
        useraddress = useraddress.userprofileaddress_set.filter(is_primary=True).first()
        pajak_beli = float(api_key) * float(produk.harga)
        pajak_beli_total = pajak_beli + float(produk.harga)
        prosentase = float(api_key) * 100
        data = {
            'alamat': useraddress,
            'produk': produk,
            'jumlah_pajak': pajak_beli,
            'total_pajak': pajak_beli_total,
            'prosentase': prosentase
        }
        return render(request, 'checkout/home_beli.html', data)
    
    def post(self, request, id):
        produk = Produk.objects.get(pk=id)
        cart = Cart.objects.create(
            user = request.user,
            expedisi = request.POST.get("expedisi"),
            tanggal=datetime.datetime.now()
        )
        cart.save()

        produk_cart = ProdukChartItem(
            store=produk.store,
            nama=produk.nama,
            harga=produk.harga,
            detail=produk.detail,
            stok_produk=produk.stok_produk,
            is_active=produk.is_active,
            stok=produk.stok,
            is_promo=produk.is_promo,
            berat=produk.berat,
            lebar=produk.lebar,
            slug=produk.slug,
            created_at=produk.created_at
        )
        produk_cart.save()
        produk_cart.kategori.set(produk.kategori.all())
        produk_cart.tipe.set(produk.tipe.all())
        produk_cart.warna.set(produk.warna.all())

        user_cart = UserCartItem()
        user_cart.nama = request.user.nama
        user_cart.no_telepon = request.user.no_telepon
        user_cart.save()
        user_cart = UserCartItem.objects.get(pk=user_cart.id)

        addr_user = UserProfileAddress.objects.filter(userprofile_id=request.user.pk, is_primary=True).first()
        user_cart_address = AddressUserChartItem()
        user_cart_address.address = addr_user.address
        user_cart_address.province = addr_user.province
        user_cart_address.distric = addr_user.distric
        user_cart_address.regency = addr_user.regency
        user_cart_address.village = addr_user.village
        user_cart_address.zipcode = addr_user.zipcode
        user_cart_address.userprofile = user_cart
        user_cart_address.typeaddress = addr_user.typeaddress
        user_cart_address.rt = addr_user.rt
        user_cart_address.rw = addr_user.rw
        user_cart_address.save()

        store_produk = UserStore.objects.filter(pk=produk.store.id).first()
        store_cart = StoreCartItem()
        store_cart.users = user_cart
        store_cart.nama = store_produk.nama
        store_cart.coin = store_produk.coin
        store_cart.deskripsi = store_produk.deskripsi
        store_cart.save()

        cart_item = CartItem.objects.create(
            cart=cart,
            produk=produk,
            produk_chart=produk_cart,
            user_chart=user_cart,
            store_chart=store_cart
        )
        cart_item.save()

        return redirect('/beli/'+str(cart.id))


@method_decorator(login_required(login_url='/profile'), name='dispatch')
class Beli(FrontPage):
    def get(self, request, id):
        profile = request.user
        alamat = UserProfileAddress.objects.filter(userprofile_id=profile.pk, is_primary=True)
        alamat = alamat.first()
        # pajak = SettingWebsite.objects.filter(nama_pengaturan=3).first()
        pajak = self.configuration.pajak_beli
        pajak_persen = float(pajak) * 100
        cart_data = None
        try:
            cart = Cart.objects.get(user_id=request.user.id, status_pembayaran=1, pk=id)
            cart_data = CartItem.objects.filter(cart__user=request.user, cart__status_pembayaran=1).latest('pk')
            jumlah = 0
            harga = cart_data.jumlah * cart_data.produk.harga
            jumlah = jumlah+harga
            ppn = 0
            if jumlah > 0:
                ppn = float(pajak) * jumlah
            jumlah_ppn = jumlah+ppn
        except Exception as e:
            print(e)
            cart = None
            cart_data = None
            jumlah = 0
            ppn=0
            jumlah_ppn=0
        return render(request, 'checkout/checkout_proses.html',{ "cart":cart,"cart_item":cart_data, "jumlah": jumlah, "ppn":ppn, "jumlah_ppn":jumlah_ppn, "prosentase": pajak_persen, "alamat": alamat })

@method_decorator(login_required(login_url='/profile'), name='dispatch')
class MinusPluss(FrontPage):
    def get(self, request):
        data = None
        try:
            cart_data = CartItem.objects.filter(cart__user_id=request.user.id, cart__status=1).first()
            typerequest = request.GET.get("type_request")
            if typerequest == "plus":
                cart_data.jumlah = cart_data.jumlah + 1
            else:
                cart_data.jumlah = cart_data.jumlah - 1
            cart_data.save()
            data = {
                "nama_produk":cart_data.produk.nama,
                "jumlah": cart_data.jumlah,
                "harga": cart_data.produk.harga,
                "kategori": [c.id for c in cart_data.produk.kategori.all()]
            }
        except Exception as e:
            print(e)
            cart_data = None
        return JsonResponse({"data":data})
        

@method_decorator(login_required(login_url='/profile'), name='dispatch')
class Settings(FrontPage):
    def get(self, request):
        return render(request, 'setting.html')

class Profile(FrontPage):
    def get(self, request):
        pesanan = None
        profile = request.user
        try:
            pesanan = {
                "pesanan":  Cart.objects.filter(status=2, status_toko=1, user=request.user.id).count(),
                "diproses" : Cart.objects.filter(status=2, status_toko=2, user=request.user.id).count(),
                "dikirim": Cart.objects.filter(status=2, status_toko=3, user=request.user.id).count(),
            }
        except Exception as e:
            pesanan = {
                "pesanan": 0,
                "diproses": 0,
                "dikirim": 0
            }
        datas = {
            "status_pesanan": pesanan,
            "profile": profile
        }
        return render(request, 'profil/profile.html', datas)

class WithdrawlToko(FrontPage):
    def get(self, request, id):
        toko = UserStore.objects.get(users_id=id)
        historywd = UserStoreWdHistory.objects.all().order_by('-pk')
        return render(request, 'toko/withdrawl.html',{"toko": toko, "history": historywd})

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
                        token=str(user.fcm_token)
                    )
                    messa = messaging.send(message)
                    print(type(user.fcm_token), messa)

                return JsonResponse({"success": True})
        return JsonResponse({"success": False})

class Tutorial(FrontPage):
    def get(self, request):
        return render(request, 'tutorial.html',{})

class PrivacyAndPolicy(FrontPage):
    def get(self, request):
        return render(request, 'privacyandpolicy.html',{})

class AboutApp(FrontPage):
    def get(self, request):
        return render(request, 'aboutapps.html',{})

class CoreTeam(FrontPage):
    def get(self, request):
        return render(request, 'coreteam.html',{})

class TermOfService(FrontPage):
    def get(self, request):
        return render(request, 'termofservice.html',{})

class SocialMedia(FrontPage):
    def get(self, request):
        return render(request, 'socialmedia.html',{})

class Tentang(FrontPage):
    def get(self, request):
        return render(request, 'tentang.html',{})

class Promo(FrontPage):
    def get(self, request):
        produk = Produk.objects.all()[:10]
        return render(request,'promo.html',{"produk": produk})

class Approve(FrontPage):
    def get(self, request, id):
        # settingweb = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        print(self.configuration.api_key_pi)
        settingweb = self.configuration.api_key_pi
        header = {"Authorization":"Key "+settingweb}
        postdata = requests.post('https://api.minepi.com/v2/payments/'+id+'/approve', headers=header)
        if postdata.status_code == 200:
            return JsonResponse(postdata.json())
        else:
            return JsonResponse({"status":False, "message": postdata.json()})

class CompletePayment(FrontPage):
    def get(self, request, id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        complete = pi.complete_payment(id)
    
class SetComplete(FrontPage):
    def completepayment(self, request, id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        complete = pi.complete_payment(id)

    def get(self, request, id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi
        datas = {"txid":request.GET.get("txid")}
        postdata = requests.post('https://api.minepi.com/v2/payments/'+id+'/complete',data=datas, headers={"Authorization":"Key "+api_key})
        if postdata.status_code == 200:
            cart = Cart.objects.get(pk=request.GET.get('id'))
            cart.status = 2
            cart.save()
            return JsonResponse({"status":True})
        else:
            return JsonResponse({"status":False})

class Faq(FrontPage):
    def get(self, request):
        return render(request, 'faq.html')

class Cancel(FrontPage):
    def get(self, request, id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi
        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi
        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        # cancel = pi.cancel_payment("zrRkKF8BrlrxrDd7of6lhCFfHvnq")
        cancel = requests.get('https://api.minepi.com/payments/'+id+'/cancel', headers={"Authorization":"Key "+api_key})
        print(cancel.json())
        return JsonResponse(cancel, safe=False)

class GetData(FrontPage):
    def get(self, request):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        # pi.cancel_payment("7SGJCpWlXOyNF91nzaysBhOZ5DBN")

        # payment_data = {
        #     "amount": 10.14,
        #     "memo": "Test - Greetings from MyApp",
        #     "metadata": {"product_id": "apple-pie-1"},
        #     "uid": "83eb8298-b7aa-46b9-b447-0ed3157f03df"
        # }
        # paymantcreate = pi.create_payment(payment_data)
        # pay = pi.submit_payment(paymantcreate, False)
        # print("================================")
        # print(paymantcreate)
        # print(pay)
        # print("=============================")
        # pi.complete_payment("ZUmPeCug4qcAljkF9IDJZrhib0hC","65c158038d4ef968026b8d33430188bd8f88237d9836bb3fee0f21ba5b885610")
        # pi.get_incomplete_server_payments()
        # payment = pi.complete_payment("7SGJCpWlXOyNF91nzaysBhOZ5DBN", "cdd9774580282c774d3364c663a82878a6bed936467332fe95eaac2a31cc11bc")
        # print(pi.get_payment("7SGJCpWlXOyNF91nzaysBhOZ5DBN"))
        # data = pi.get_incomplete_server_payments()
        # pi.cancel_payment('pQfMlQLbuSI0I1uhrC85F30jK69q')
        # try:
        #     print(pay)
        # except Exception as e:
        #     print(e)
        # for p in data:
        #     # print(p['identifier'])
        #     pi.cancel_payment(p['identifier'])
        #     # txid = pi.submit_payment(p['identifier'], True)
        #     # print(txid)
        return JsonResponse({ "data":True })

class CartJson(FrontPage):
    def get(self, request, id):
        cartitem = CartItem.objects.filter(pk=id).first()
        # pajak = SettingWebsite.objects.filter(nama_pengaturan=3).first()
        pajak = float(self.configuration.pajak_beli)
        pajak_persen = float(pajak) * 100
        data = { "success": False }
        if cartitem:
            barang_harga = cartitem.produk.harga
            barang_jumlah = cartitem.jumlah
            barang_total = barang_harga * barang_jumlah
            barang_pajak = barang_total * pajak
            harga_total = barang_total + barang_pajak
            data = { "success": True, "harga_total":harga_total, "barang_total":barang_total }
        return JsonResponse(data)

class PaymentCartCancel(FrontPage):
    def get(self, request, param_id):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        # wallet_private_seed = SettingWebsite.objects.filter(nama_pengaturan=2).first()
        wallet_private_seed = self.configuration.wallet_private_pi

        pi = PiNetwork()
        pi.initialize(api_key, wallet_private_seed, self.pinetwork_type)
        cancel = pi.cancel_payment_user(param_id)
        return JsonResponse(cancel, safe=False)


class PaymentsCart(FrontPage):
    def setcomplete(self, request ,cart_id, identifier, param):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi
        datas = {"txid":param}

        postdata = requests.post(
            'https://api.minepi.com/v2/payments/'+identifier+'/complete',data=datas, 
            headers={"Authorization":"Key "+api_key}
        )

        if postdata.status_code == 200:
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
            return {"status":True}
        else:
            return {"status":False}

    def get(self, request, param):
        # api_key = SettingWebsite.objects.filter(nama_pengaturan=1).first()
        api_key = self.configuration.api_key_pi

        data_url = "https://api.minepi.com/v2/payments/"+param
        requestdata = requests.get(
            data_url, 
            headers={ 'Authorization': 'Key '+api_key}
        )

        cart_id = request.GET.get("cart_id")
        requestjson = requestdata.json()
        result_dict = json.loads(str(json.dumps(requestjson)))
        try:
            carts = CartItem.objects.get(pk=cart_id)
            print(carts, cart_id)
            # cartitems = CartItem.objects.get(cart__id=carts.id)
            # print(carts, cartitems)
            subject = 'Payment Success GeraiPi'
            html_message = render_to_string('mail_template.html', {"carts": carts})
            plain_message = strip_tags(html_message)
            from_email = 'From <payment@geraipi.id>'
            to = request.user.email
            # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            msg = EmailMessage(subject, html_message, from_email,[to])
            msg.content_subtype = "html"
            msg.send()

        except CartItem.DoesNotExist or Exception as e:
            print(e)

        txid = result_dict.get("transaction")
        txid = json.loads(str(json.dumps(txid)))
        txid = txid.get("txid")
        t = self.setcomplete(request, cart_id, param, txid)
        return JsonResponse(t, safe=False)

class TransaksiUserSelesaiJson(FrontPage):
    def get(self, request):
        cart_id = request.GET.get("cart_id", None)
        try:
            if cart_id:
                cartitem = CartItem.objects.get(pk=cart_id)
                
                carts = Cart.objects.get(pk=cartitem.cart.id)
                carts.status=4
                carts.status_toko=4
                carts.save()

                userprofile = UserStore.objects.get(pk=cartitem.produk.store.id)
                userprofile.coin += float(cartitem.jumlah) * float(cartitem.produk.harga)
                userprofile.save()
        except Exception as e:
            print(e)
        return JsonResponse({"success": True}, safe=False)

class DetailTransaksiJson(FrontPage):
    def get(self, request):
        cartitem = CartItem.objects.filter(pk=request.GET.get("detail", 0)).first()
        data = {
            "success": True,
            "data":{
                "cart": cartitem.cart.kode,
                "tanggal": cartitem.cart.tanggal.date(),
                "jumlah": cartitem.jumlah,
                "resi": cartitem.cart.nomor_resi,
                "produk": {
                    "nama_produk": cartitem.produk.nama,
                    "harga": cartitem.produk_chart.harga
                }
            }
        }
        return JsonResponse(data)

class DetailTransaksi(FrontPage):
    def get(self, request):
        cart = Cart.objects.get(pk=request.GET.get("detail"))
        data = {
            "transaksi": cart
        }
        return render(request, 'profil/transaksi_detail.html', data)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class DetailTransaksiUlasan(FrontPage):
    def post(self, request, id):
        cart = Cart.objects.get(pk=id)
        cartitem = CartItem.objects.get(cart_id=cart.id)
        ulasan = UlasanCart.objects.filter(cart_id=id).first()
        if not ulasan:
            ulasan = UlasanCart()
        ulasan.produk = request.POST.get('rating_produk',0)
        ulasan.catatan = request.POST.get('catatan_produk',"-")
        ulasan.cart = cart
        ulasan.produkitem = cartitem.produk
        ulasan.save()
        return redirect(reverse("detail_transaksi_user_ulasan", kwargs={"id":id}))
    
    def get(self, request, id):
        cart = Cart.objects.get(pk=id)
        ulasan = UlasanCart.objects.filter(cart_id=id).first()
        data = {
            "cart": cart,
            "ulasan": ulasan,
            "range_value": range(1, 6)
        }
        return render(request, 'profil/ulasan_transaksi.html', data)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class EditBarang(FrontPage):
    def get(self, request, id, produk_id):
        produk = Produk.objects.filter(pk=produk_id).first()
        image = {
            "gambar1": None,
            "gambar2": None,
            "gambar3": None
        }
        if produk.gambarproduk_set:
            produks_image = produk.gambarproduk_set.all()
            gambar_number = 1
            for gambar in produks_image:
                image.update({"gambar"+str(gambar_number): gambar.gambar})
                gambar_number += 1
        kategori = Kategori.objects.all()
        tipe = TipeProduk.objects.all()
        warna = WarnaProduk.objects.all()
        data = {
            'data': produk,
            "images": image,
            "kategori": kategori,
            "typeproduk": tipe,
            "warnaproduk": warna
        }
        return render(request, 'toko/edit_barang.html', data)

    def post(self, request, id, produk_id):
        produk = Produk.objects.filter(pk=produk_id).first()
        image = {
            "gambar1": None,
            "gambar2": None,
            "gambar3": None
        }
        if produk.gambarproduk_set:
            produks_image = produk.gambarproduk_set.all()
            gambar_number = 1
            for gambar in produks_image:
                image.update({"gambar"+str(gambar_number): gambar.gambar})
                gambar_number += 1
        kategori = Kategori.objects.all()
        tipe = TipeProduk.objects.all()
        warna = WarnaProduk.objects.all()

        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        stok = request.POST.get('stok')
        harga = request.POST.get('harga')
        kategori_post = request.POST.getlist('kategori')
        tipe_post = request.POST.getlist('tipe')
        warna_post = request.POST.getlist('warna')
        berat = request.POST.get('berat')
        lebar = request.POST.get('lebar')

        produk.nama = nama
        produk.detail = deskripsi
        produk.stok_produk = stok
        produk.harga = harga
        produk.berat = berat
        produk.lebar = lebar
        produk.save()

        produk.kategori.remove()
        produk.tipe.remove()
        produk.warna.remove()

        for k in kategori_post:
            kateg = Kategori.objects.filter(pk=k).first()
            produk.kategori.add(kateg)

        for k in warna_post:
            warna = None
            try:
                warnaa = WarnaProduk.objects.filter(pk=k).first()
            except Exception as e:
                warnaa = WarnaProduk.objects.filter(nama=k).first()
            if warnaa:
                produk.warna.add(warnaa)
            else:
                warnaa = WarnaProduk.objects.create(nama=k)
                produk.warna.add(warnaa)
        tipes = TipeProduk.objects.filter(pk__in=tipe_post).first()
        produk.tipe.add(tipes)
        
        filess1 = request.FILES.get('gambar1')
        filess2 = request.FILES.get('gambar2')
        filess3 = request.FILES.get('gambar3')
        
        if filess1:
            gproduk = GambarProduk.objects.filter(sortings=1, produk_id=produk.pk).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=1,
                    produk=produk, 
                    nama=nama, 
                    gambar=filess1
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess1
                gproduk.save()
        
        if filess2:
            gproduk = GambarProduk.objects.filter(sortings=2, produk_id=produk.pk).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=2,
                    produk=produk, 
                    nama=nama, 
                    gambar=filess2
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess2
                gproduk.save()
        
        if filess3:
            gproduk = GambarProduk.objects.filter(sortings=3, produk_id=produk.pk).first()
            if not gproduk:
                GambarProduk.objects.create(
                    sortings=3,
                    produk=produk, 
                    nama=nama, 
                    gambar=filess3
                )
            else:
                gproduk.nama = nama
                gproduk.gambar = filess3
                gproduk.save()
        return redirect('/toko/{}/list_produk/'.format(str(id)))

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class ArchiveBarang(FrontPage):
    def post(self, request, id, produk_id):
        produk = Produk.objects.get(pk=produk_id)
        produk.is_archive = True
        produk.save()
        return redirect('/toko/{}/list_produk/'.format(str(id)))

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required(login_url='/profile'), name='dispatch')
class TransaksiToko(FrontPage):
    def post(self, request, id):
        status = request.GET.get("status", 1)
        if status:
            cart = Cart.objects.get(pk=request.POST.get("cart_id"))
            # for c in cart:
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
                else:
                    messages.error(request,"Sorry, please input your number")
                    return redirect("/toko/"+str(request.user.id)+"/transaksi/?status=2")
            elif cart.status_toko == 3:
                cart.status=3
                cart.tanggal_selesai = datetime.datetime.now()
                # cart.status_toko = 4
            cart.save()
        return redirect("/toko/"+str(request.user.id)+"/transaksi/")
        
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
                cart__status_pembayaran=2
            )
            context.update({ "produk": produk })
        context.update({
            "pesanan": CartItem.objects.filter(cart__status_toko=1, produk__store_id=store.id, cart__status_pembayaran=2).count(),
            "diproses": CartItem.objects.filter(cart__status_toko=2, produk__store_id=store.id, cart__status_pembayaran=2).count(),
            "dikirim": CartItem.objects.filter(cart__status_toko=3, produk__store_id=store.id, cart__status_pembayaran=2).count(),
        })
        return render(request, "toko/listtransaksi.html", context)

    # Profile 
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AlamatUser(FrontPage):
    def post(self, request, id, type):
        types = None
        typeid = None
        if type == "domestic":
            types = "Domestic"
            typeid = 1
        else:
            types = "Non Domestic"
            typeid = 2

        
        userprofile = request.user
        userprofileaddress = UserProfileAddress.objects.filter(userprofile_id=request.user.id)

        userdetail = UserProfileAddress()
        userdetail.address = request.POST.get("address",None)
        userdetail.zipcode = request.POST.get("zipcode",None)
        userdetail.rt = request.POST.get("rt",None)
        userdetail.rw = request.POST.get("rw",None)
        userdetail.province_id = request.POST.get("province",None)
        userdetail.regency_id = request.POST.get("regency",None)
        userdetail.distric_id = request.POST.get("distric",None)
        userdetail.userprofile_id = userprofile.pk
        userdetail.save()

        return redirect("/profile/alamat")
    
    def get(self, request, id, type):
        types = None
        typeid = None
        if type == "domestic":
            types = "Domestic"
            typeid = 1
        else:
            types = "Non Domestic"
            typeid = 2
        userprofile = request.user
        userprofileaddress = UserProfileAddress.objects.filter(userprofile_id=request.user.id)
        return render(request, 'profil/profile_alamat.html', {"type":types, "typeid": typeid, "address": userprofileaddress})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DetailProfile(FrontPage):
    def get(self, request):
        profile = request.user
        try:
            useraddress = UserProfileAddress.objects.filter(userprofile_id = profile.id)
        except UserProfileAddress.DoesNotExist:
            useraddress = None
        datas = {
            "address": useraddress,
        }
        return render(request, 'profil/detail_profile.html', datas)
    
    def post(self, request):
        userss = request.user
        try:
            usernames = UserProfileAddress.objects.filter(userprofile_id=userss.id, pk=request.POST.get('id')).first()
            usernames.is_primary = True
            usernames.save()

            usernames = UserProfileAddress.objects.filter(userprofile_id=userss.id).exclude(pk=request.POST.get('id'))
            for a in usernames:
                a.is_primary = False
                a.save()
            
        except UserProfile.DoesNotExist:
            usernames = None
        return redirect('/profile/alamat')
        
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteDetailProfile(FrontPage):
    def post(self, request, id_alamat):
        useralamat = UserProfileAddress.objects.get(pk=id_alamat)
        useralamat.delete()
        return redirect('/profile/alamat')

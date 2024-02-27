"""
URL configuration for projekpi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path
from rest_framework import routers

from frontend.viewsets import (DistricViewset, GambarProdukViewSet,
                               KategoriViewSet, ProdukViewSet, ProvinsiViewset,
                               RegencyViewset, UserAddressViewset,
                               UserProfileViewset, UserViewSet,
                               VillagerViewset)

from .function_view.detail_view import Detail
from .function_view.fcm_save_token import FcmSaveTokenView
from .function_view.home import Home
from .function_view.keranjang_add_view import KeranjangAdd
from .function_view.koleksi_view import Koleksi
from .function_view.list_produk_toko_view import ListProdukToko
from .function_view.login_user_view import LoginUser
from .function_view.masuk_view import Masuk
from .function_view.produk_view import Produks
from .function_view.profile_edit_view import ProfileEdit
from .function_view.save_token_views import SaveToken
from .function_view.search_produk_view import SearchProduct
from .function_view.service_worker import ServiceWorkerView
from .function_view.splash import Splash
from .function_view.toko_view import Toko
from .function_view.transaksi_user_count_json_view import \
    TransaksiUserCountJson
from .function_view.transaksi_user_json_view import TransaksiUserJson
from .function_view.transaksi_user_view import TransaksiUsers
from .function_view.translated_view import TranslatedApi
from .function_view.withdrawl_proccess_view import WithdrawlProcess
from .function_view.withdrawl_request_json_view import WithdrawlRequestJson
from .function_view.withdrawl_view import Withdrawl
from .views import (AboutApp, AddToCart, AlamatToko, AlamatTokoTambah,
                    AlamatUser, Approve, ArchiveBarang, Beli, Cancel, CartJson,
                    CompletePayment, CoreTeam, DeleteAlamatToko,
                    DeleteDetailProfile, DetailProfile,
                    DetailProfileAddressMain, DetailTransaksi,
                    DetailTransaksiJson, DetailTransaksiUlasan, EditBarang,
                    Faq, GetData, Jual, MinusPluss, PaymentCartCancel,
                    PaymentsCart, PrivacyAndPolicy, Profile, Promo,
                    SetComplete, Settings, Tentang, TermOfService,
                    TransaksiToko, TransaksiUserSelesaiJson, Tutorial,
                    UploadDropzone, WithdrawlToko, WithdrawlTokoJson)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"produks", ProdukViewSet)
router.register(r"kategoris", KategoriViewSet)
router.register(r"provinsis", ProvinsiViewset)
router.register(r"districs", DistricViewset)
router.register(r"regencys", RegencyViewset)
router.register(r"villages", VillagerViewset)
router.register(r"user-profiles", UserProfileViewset)
router.register(r"user-address", UserAddressViewset)

urlpatterns = [
    path("", Splash.as_view(), name="splash"),
    path("home", Home.as_view(), name="home"),
    path("produk/", Produks.as_view(), name="produk"),
    path("save_token", SaveToken.as_view(), name="save_token"),
    path("keranjang/add/<int:id>", KeranjangAdd.as_view(), name="keranjang_add"),
    path("search_product", SearchProduct.as_view(), name="search_product"),
    # profile
    path("profile", Profile.as_view(), name="profile"),
    path("profiles/edit", ProfileEdit.as_view(), name="profiles_edit"),
    path("profile/alamat", DetailProfile.as_view(), name="profile_detail"),
    path(
        "profile/alamat/<int:id_alamat>/delete",
        DeleteDetailProfile.as_view(),
        name="delete_profile_detail",
    ),
    path("transaksi/users/list", TransaksiUsers.as_view(), name="transaksi_users"),
    # checkout
    path("keranjang/<int:id>", AddToCart.as_view(), name="addkeranjang"),
    path("beli/<int:id>", Beli.as_view(), name="beli"),
    path("transaksi/detail", DetailTransaksi.as_view(), name="detail_transaksi_user"),
    path(
        "transaksi/detail/<int:id>/ulasan",
        DetailTransaksiUlasan.as_view(),
        name="detail_transaksi_user_ulasan",
    ),
    # toko
    path("toko/<int:id>/", Toko.as_view(), name="toko"),
    path(
        "toko/<int:id>/list_produk/", ListProdukToko.as_view(), name="list_produk_toko"
    ),
    path(
        "toko/<int:id>/produk/<int:produk_id>/edit",
        EditBarang.as_view(),
        name="edit_barang",
    ),
    path(
        "toko/<int:id>/produk/<int:produk_id>/delete",
        ArchiveBarang.as_view(),
        name="delete_barang",
    ),
    path("toko/<int:id>/alamat/", AlamatToko.as_view(), name="alamat_toko"),
    path(
        "toko/<int:id>/alamat/<int:id_alamat>/delete",
        DeleteAlamatToko.as_view(),
        name="delete_alamat_toko",
    ),
    path(
        "toko/<int:id>/alamat/tambah",
        AlamatTokoTambah.as_view(),
        name="tambah_alamat_toko",
    ),
    path("toko/<int:id>/withdrawl", WithdrawlToko.as_view(), name="withdrawl_toko"),
    path(
        "toko/<int:id>/withdrawl/json",
        WithdrawlTokoJson.as_view(),
        name="withdrawl_toko_json",
    ),
    path("toko/<int:id>/transaksi/", TransaksiToko.as_view(), name="transaksi_toko"),
    # user
    path("user/withdrawl/", Withdrawl.as_view(), name="withdrawl"),
    path(
        "user/withdrawl/process/json",
        WithdrawlProcess.as_view(),
        name="widrawl_process",
    ),
    path(
        "user/withdrawl/request/process/json",
        WithdrawlRequestJson.as_view(),
        name="widrawl_request_process",
    ),
    path(
        "tambah/alamat/<int:id>/<str:type>",
        AlamatUser.as_view(),
        name="tambah_alamat_user",
    ),
    path("masuk", Masuk.as_view(), name="masuk"),
    path("tutorial", Tutorial.as_view(), name="tutorial"),
    path("privacy-and-policy", PrivacyAndPolicy.as_view(), name="privacyandpolicy"),
    path("aboutapps", AboutApp.as_view(), name="aboutapps"),
    path("coreteam", CoreTeam.as_view(), name="coreteam"),
    path("tos", TermOfService.as_view(), name="termofservice"),
    path("tentang", Tentang.as_view(), name="tentang"),
    path("setting", Settings.as_view(), name="settings"),
    path("koleksi/<str:nama_toko>", Koleksi.as_view(), name="koleksi"),
    path(
        "address/user/<int:id>",
        DetailProfileAddressMain.as_view(),
        name="address_userprofile",
    ),
    path("balance", GetData.as_view(), name="balance"),
    path("login_user/", LoginUser.as_view(), name="login_user"),
    path("minusplus/", MinusPluss.as_view(), name="minus_plus"),
    path("jual/", Jual.as_view(), name="jual"),
    path("batal/<str:id>", Cancel.as_view(), name="batal_cart"),
    path("paymentchart/<str:param>", PaymentsCart.as_view(), name="payment_cart"),
    path("cart_json/<int:id>", CartJson.as_view(), name="cart_json"),
    path("setcomplete/<str:id>", SetComplete.as_view(), name="setcomplete"),
    path("produk/detail/<str:slug>", Detail.as_view(), name="detail_produk"),
    path("file/post", UploadDropzone.as_view(), name="upload_dropzone"),
    path("promo/", Promo.as_view(), name="promo"),
    path("approve/<str:id>", Approve.as_view(), name="approve"),
    path("cancel/<str:id>", Cancel.as_view(), name="cancel"),
    path("completing/<str:id>", CompletePayment.as_view(), name="completing"),
    path("faq/", Faq.as_view(), name="faq"),
    path("api/v1/", include(router.urls)),
    path(
        "transaksi/users/list/json",
        TransaksiUserJson.as_view(),
        name="transaksi_users_json",
    ),
    path(
        "transaksi/users/list/count/json",
        TransaksiUserCountJson.as_view(),
        name="transaksi_users_count_json",
    ),
    path(
        "transaksi/detail/json",
        DetailTransaksiJson.as_view(),
        name="detail_transaksi_user_json",
    ),
    path(
        "transaksi/users/selesai/json",
        TransaksiUserSelesaiJson.as_view(),
        name="transaksi_users_selesai_json",
    ),
    path("translate/json", TranslatedApi.as_view(), name="translated_json"),
    # firebase
    path(
        "firebase-messaging-sw.js", ServiceWorkerView.as_view(), name="service_worker"
    ),
    path("fcm-token", FcmSaveTokenView.as_view(), name="fcm_token"),
]

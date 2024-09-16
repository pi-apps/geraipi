from django.urls import path

from frontend.views.aboutapp_view import AboutApp
from frontend.views.add_to_cart_view import AddToCart
from frontend.views.alamat_toko_delete_view import DeleteAlamatToko
from frontend.views.alamat_toko_view import AlamatToko
from frontend.views.alamt_toko_tambah_view import AlamatTokoTambah
from frontend.views.approve_view import Approve
from frontend.views.archive_barang_view import ArchiveBarang
from frontend.views.beli_view import Beli
from frontend.views.beranda.home import Home
from frontend.views.cancel_view import Cancel
from frontend.views.cart_json_view import CartJson
from frontend.views.completepayment_view import CompletePayment
from frontend.views.coreteam_view import CoreTeam
from frontend.views.detail_transaksi_json_view import DetailTransaksiJson
from frontend.views.detail_transaksi_usulan_view import DetailTransaksiUlasan
from frontend.views.detail_transaksi_view import DetailTransaksi
from frontend.views.dropzone_upload_view import UploadDropzone
from frontend.views.edit_barang_view import EditBarang
from frontend.views.faq_view import Faq
from frontend.views.fcm_save_token import FcmSaveTokenView
from frontend.views.getdata_view import GetData
from frontend.views.jual_view import Jual
from frontend.views.keranjang_add_view import KeranjangAdd
from frontend.views.koleksi_view import Koleksi
from frontend.views.list_produk_toko_view import ListProdukToko
from frontend.views.login_user_view import LoginUser
from frontend.views.masuk_view import Masuk
from frontend.views.minus_plus_view import MinusPluss
from frontend.views.payments_cart_view import PaymentsCart
from frontend.views.piverification_view import VerificationCode
from frontend.views.privacyandpolicy_view import PrivacyAndPolicy
from frontend.views.produk.produk_detail_view import ProdukDetail

# produk
from frontend.views.produk.produk_view import Produks
from frontend.views.profile.alamat_user_view import AlamatUser
from frontend.views.profile.profile_alamat_view import ProfileAlamat
from frontend.views.profile.profile_edit_view import ProfileEdit
from frontend.views.profile.profile_view import Profile
from frontend.views.profile.register_member import RegisterMember
from frontend.views.profile.register_member_code import RegisterMemberCode
from frontend.views.profile_delete_detail_view import DeleteDetailProfile
from frontend.views.profile_detail_address_view import DetailProfileAddressMain
from frontend.views.promo_view import Promo
from frontend.views.save_token_views import SaveToken
from frontend.views.search_produk_view import SearchProduct
from frontend.views.service_worker import ServiceWorkerView
from frontend.views.setcomplete_view import SetComplete
from frontend.views.settings_view import Settings
from frontend.views.splash import Splash
from frontend.views.tentang_view import Tentang
from frontend.views.termofservice_view import TermOfService
from frontend.views.toko.toko_view import Toko
from frontend.views.toko_edit_view import TokoEdit
from frontend.views.toko_transaksi_view import TransaksiToko
from frontend.views.transaksi_selesai_view import TransaksiUserSelesaiJson
from frontend.views.transaksi_user_count_json_view import TransaksiUserCountJson
from frontend.views.transaksi_user_json_view import TransaksiUserJson
from frontend.views.transaksi_user_view import TransaksiUsers
from frontend.views.translated_view import TranslatedApi
from frontend.views.tutorial_view import Tutorial
from frontend.views.withdrawl_proccess_view import WithdrawlProcess
from frontend.views.withdrawl_request_json_view import WithdrawlRequestJson
from frontend.views.withdrawl_toko_view import WithdrawlToko
from frontend.views.withdrawl_view import Withdrawl
from frontend.views.withdrawltokojson_view import WithdrawlTokoJson

urlpatterns = [
    path("", Splash.as_view(), name="splash"),
    path("home", Home.as_view(), name="home"),
    path("produk/", Produks.as_view(), name="produk"),
    path("produk/<str:slug>", ProdukDetail.as_view(), name="produk_detail"),
    path("save_token", SaveToken.as_view(), name="save_token"),
    path("keranjang/add/<int:id>", KeranjangAdd.as_view(), name="keranjang_add"),
    path("search_product", SearchProduct.as_view(), name="search_product"),
    # profile
    path("profile", Profile.as_view(), name="profile"),
    path("profiles/edit", ProfileEdit.as_view(), name="profiles_edit"),
    path("profile/alamat", ProfileAlamat.as_view(), name="profile_detail"),
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
    path("toko/<int:id>/profile/edit", TokoEdit.as_view(), name="toko_profile_edit"),
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
        "tambah/alamat",
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
    path("file/post", UploadDropzone.as_view(), name="upload_dropzone"),
    path("promo/", Promo.as_view(), name="promo"),
    path("approve/<str:id>", Approve.as_view(), name="approve"),
    path("cancel/<str:id>", Cancel.as_view(), name="cancel"),
    path("completing/<str:id>", CompletePayment.as_view(), name="completing"),
    path("faq/", Faq.as_view(), name="faq"),
    path("member/", RegisterMember.as_view(), name="register_member"),
    path("member/code/", RegisterMemberCode.as_view(), name="register_member_code"),
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
    path("validation-key.txt", VerificationCode.as_view(), name="verification"),
]

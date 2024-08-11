from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.urls import path, reverse
from django.urls.resolvers import URLPattern
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt

from profiles.models import (
    LangSupport,
    Tier,
    UserAppliedMember,
    UserCodeGenerator,
    UserProfile,
    UserProfileAddress,
    UserSettingsMember,
    UserWithdrawlTransaction,
    UserwithdrawlTransactionRequest,
)
from store.models import UserStore


# Register your models here.
class ProfileAdmin(UserAdmin):
    change_form_template = "loginas/change_form.html"
    list_display = ("username", "email", "no_telepon", "fcm_token")
    fieldsets = [
        (
            "General",
            {
                "fields": [
                    "username",
                    "password",
                    "no_telepon",
                    "fcm_token",
                    "language",
                    "typeuser",
                    "languages",
                    "coin",
                ],
            },
        ),
        (
            "Personal Info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "wallet",
                    "image_profile",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ),
    ]

    @csrf_exempt
    def json_profiles(self, request):
        data = {"success": False}
        modelresponse = UserProfile.objects.filter(users_id=request.user.id)
        if request.method == "POST":
            modelresponse = modelresponse.first()
            modelresponse.nama = request.POST.get("name", "")
            modelresponse.wallet = request.POST.get("wallet", "")
            modelresponse.no_telepon = request.POST.get("no_telepon", "")
            modelresponse.save()
            user = request.user
            user.email = request.POST.get("email", "")
            user.save()
            data.update(
                {
                    "success": True,
                    "data": {
                        "name": modelresponse.nama,
                        "wallet": modelresponse.wallet,
                        "no_telepon": modelresponse.no_telepon,
                        "email": request.user.email,
                    },
                }
            )
        else:
            if modelresponse.exists():
                modelresponse = modelresponse.first()
                data.update(
                    {
                        "data": {
                            "name": modelresponse.nama,
                            "wallet": modelresponse.wallet,
                            "no_telepon": modelresponse.no_telepon,
                            "email": request.user.email,
                        }
                    }
                )
        return JsonResponse(data)

    def get_urls(self) -> list[URLPattern]:
        super_url = super().get_urls()
        base_name = "profiles_"
        super_url = [
            path(
                "json_profile_admin",
                self.admin_site.admin_view(self.json_profiles),
                name=base_name + "json_profile",
            ),
        ] + super_url
        return super_url


admin.site.register(UserProfile, ProfileAdmin)


class UserProfileAddressAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        query = super().get_queryset(request)
        if not request.user.is_superuser:
            if "Toko" in [a.name for a in request.user.groups.all()]:
                query = query.filter(user_id=request.user.id)
        elif request.user.is_superuser:
            query = query
        else:
            query = query.none()
        return query


admin.site.register(UserProfileAddress, UserProfileAddressAdmin)


class UserWithdrawlRequestAdmin(admin.ModelAdmin):
    list_display = [
        "kode",
        "user",
        "get_user_email",
        "get_user_wallet",
        "jumlah",
        "status",
        "list_action",
    ]
    search_fields = ["kode"]

    def get_code(self, obj):
        kode = obj.kode or "-"
        return kode

    get_code.short_description = "Kode Transaksi"

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = "Email User"

    def get_user_wallet(self, obj):
        return obj.user.wallet

    get_user_wallet.short_description = "Wallet User"

    def list_action(self, obj):
        objs = "Selesai"
        if obj.status == 1:
            reverse_url = reverse(
                "admin:user_withdrawl_request_admin_json_request_action"
            )
            objs = format_html(
                '<a href="{}" class="btn btn-success btn-sm">Selesai</a>'.format(
                    reverse_url + "?id=" + str(obj.pk)
                )
            )
        return objs

    list_action.short_description = "Aksi"

    @csrf_exempt
    def json_request_action(self, request):
        modelresponse = UserwithdrawlTransactionRequest.objects.filter(
            id=request.GET.get("id")
        ).first()
        if modelresponse:
            modelresponse.status = 2
            modelresponse.save()

            if modelresponse.status == 2:
                UserWithdrawlTransaction.objects.create(
                    user=request.user, jumlah=modelresponse.jumlah
                )
                userprofile = request.user
                float_coin = float(userprofile.coin)
                float_jumlah = float(modelresponse.jumlah)
                userprofile.coin = float_coin - float_jumlah
                userprofile.save()
        return redirect(
            reverse("admin:profiles_userwithdrawltransactionrequest_changelist")
        )

    def get_urls(self) -> list[URLPattern]:
        super_url = super().get_urls()
        base_name = "user_withdrawl_request_admin_"
        super_url = [
            path(
                "withdrawl/request/json",
                self.admin_site.admin_view(self.json_request_action),
                name=base_name + "json_request_action",
            ),
        ] + super_url
        return super_url


admin.site.register(UserwithdrawlTransactionRequest, UserWithdrawlRequestAdmin)


class LangSupportAdmin(admin.ModelAdmin):
    list_display = ["code", "alias", "is_active", "is_active_store"]
    search_fields = ["code", "alias"]


admin.site.register(LangSupport, LangSupportAdmin)


class UserAppliedMemberAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "email", "nomor", "is_accept"]
    search_fields = ["name", "email"]
    list_filter = ["is_accept"]


admin.site.register(UserAppliedMember, UserAppliedMemberAdmin)


class UserCodeGeneratorAdmin(admin.ModelAdmin):
    list_display = ["user_apply_username", "code", "quota_withdrawl", "is_active"]
    search_fields = [
        "user_apply__user__username",
    ]

    def user_apply_username(self, obj):
        return obj.user_apply.user or "-"

    user_apply_username.short_description = "Username"


admin.site.register(UserCodeGenerator, UserCodeGeneratorAdmin)


class UserSettingMemberAdmin(admin.ModelAdmin):
    list_display = ["code", "user_name"]

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = "Username"

    def save_model(self, request, obj, form, change):
        userstore = UserStore.objects.filter(users_id=obj.user_id).last()
        userstore.is_active_store = obj.is_active_store
        userstore.save()
        super().save_model(request, obj, form, change)


admin.site.register(UserSettingsMember, UserSettingMemberAdmin)


class TierAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Tier, TierAdmin)

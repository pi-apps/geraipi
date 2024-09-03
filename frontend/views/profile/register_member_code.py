from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from profiles.models import (
    Tier,
    UserAppliedMember,
    UserCodeGenerator,
    UserSettingsMember,
)
from store.models import UserStore

from ..base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class RegisterMemberCode(FrontPage):
    def post(self, request):
        userprofile = request.user
        code = request.POST.get("applied")
        usercode = UserCodeGenerator.objects.filter(code=code, is_active=True)
        if usercode.exists():
            usercode = usercode.first()
            if usercode:
                quota = usercode.quota_withdrawl
                bypassing = usercode.bypass_waiting
                update_info = usercode.updated_information

                usersetting = UserSettingsMember.objects.get(user_id=request.user.id)
                if usersetting:
                    tier = Tier.objects.get(kuota_withdrawl=0)
                    usersetting = UserSettingsMember.objects.get(user_id=userprofile.id)
                    usersetting.tier = tier
                    usersetting.is_active_store = True
                    usersetting.save()
                else:
                    usersetting = UserSettingsMember()
                    usersetting.code = usercode.code
                    usersetting.bypass_waiting = bypassing
                    usersetting.updated_information = update_info
                    usersetting.quota_withdrawl = quota
                    usersetting.user = userprofile
                    usersetting.save()

                userstore = UserStore.objects.filter(users_id=userprofile.id)
                userstore = userstore.first()
                if userstore:
                    userstore.nama = userprofile.nama
                    userstore.is_active_store = True
                    userstore.aggrement = True
                    userstore.save()
                else:
                    userstore = UserStore.objects.create(
                        nama=userprofile,
                        users_id=request.user.id,
                        is_active_store=True,
                        aggrement=True,
                    )
                usercode.is_active = False
                usercode.save()
                return redirect(reverse("profile"))

    def get(self, request):
        applied = UserAppliedMember.objects.filter(
            user_id=request.user.id, is_accept=True
        )
        if not applied.exists():
            return redirect(reverse("register_member"))
        return render(request, "member/register_code_input.html")

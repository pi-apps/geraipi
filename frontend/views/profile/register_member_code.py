from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from profiles.models import UserAppliedMember
from ..base_view import FrontPage
import datetime


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class RegisterMemberCode(FrontPage):
    def post(self, request):
        userprofile = request.user
        userapplied = UserAppliedMember()
        userapplied.user = userprofile
        userapplied.is_accept = False
        userapplied.accept_date = datetime.datetime.now()
        userapplied.save()
        return redirect(reverse("register_member"))

    def get(self, request):
        applied = UserAppliedMember.objects.filter(user_id=request.user.id, is_accept=True)
        if not applied.exists():
            return redirect(reverse("register_member"))
        return render(
            request,
            "member/register_code_input.html"
        )

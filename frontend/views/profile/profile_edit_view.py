from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.view_helper import translater
from frontend.views.base_view import FrontPage
from profiles.models import LangSupport


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class ProfileEdit(FrontPage):
    def get(self, request):
        data = request.user
        data.nama = data.nama or ""
        data.no_telepon = data.no_telepon or ""
        data.email = data.email or ""
        languages = LangSupport.objects.filter(is_active=True)
        return render(request, "profil/profiles_edit.html", {"data": data, "languages": languages})

    def post(self, request):
        models = request.user
        models.email = request.POST.get("email")
        models.no_telepon = request.POST.get("no_telepon")
        models.nama = request.POST.get("nama")
        models.languages_id = request.POST.get("languages")
        models.wallet = request.POST.get("wallet")
        models.image_profile = request.FILES.get("gambars")
        models.save()
        languagescode = request.user.languages.code if request.user.languages else "en"
        message = translater(languagescode, "Sukses Menyimpan Profil", "Sukses Menyimpan Profil")
        messages.success(request, message)
        return redirect("/profiles/edit")

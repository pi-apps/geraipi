from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .base_view import FrontPage
from django.shortcuts import render, redirect
from profiles.models import LangSupport


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProfileEdit(FrontPage):
    def get(self, request):
        data = request.user
        data.nama = data.nama or ""
        data.no_telepon = data.no_telepon or ""
        data.email = data.email or ""
        languages = LangSupport.objects.all()
        return render(request, "profil/profiles_edit.html", {"data": data, "languages":languages})

    def post(self, request):
        models = request.user
        models.email = request.POST.get("email")
        models.no_telepon = request.POST.get("no_telepon")
        models.nama = request.POST.get("nama")
        models.languages_id = request.POST.get("languages")
        models.wallet = request.POST.get("wallet")
        models.save()
        return redirect('/profiles/edit')

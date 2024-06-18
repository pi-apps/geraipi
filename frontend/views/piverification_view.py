from django.shortcuts import render, HttpResponse

from frontend.views.base_view import FrontPage
from django.views import View
from master.models import ConfigurationWebsite


class VerificationCode(View):
    def get(self, request):
        config = ConfigurationWebsite.get_solo()
        return HttpResponse(config.verification or "")

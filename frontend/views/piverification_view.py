from django.shortcuts import HttpResponse, render
from django.views import View

from frontend.views.base_view import FrontPage
from master.models import ConfigurationWebsite


class VerificationCode(View):
    def get(self, request):
        config = ConfigurationWebsite.get_solo()
        return HttpResponse(config.verification or "")

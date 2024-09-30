from django.shortcuts import HttpResponse
from django.views import View

from master.models.configuration_website import ConfigurationWebsite


class VerificationCode(View):
    def get(self, request):
        config = ConfigurationWebsite.get_solo()
        return HttpResponse(config.verification or "")

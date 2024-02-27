from django.shortcuts import render
from django.http import JsonResponse
from .base_view import FrontPage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from frontend.view_helper import translater

@method_decorator(csrf_exempt, name='dispatch')
class TranslatedApi(FrontPage):
    def post(self, request):
        values = ""
        if request.POST.get("text_translate"):
            values = request.POST.get("text_translate")
        language = "id"
        if request.user.is_authenticated:
            language = request.user.languages
            if language:
                language = language.code
            else:
                language = "en"
        else:
            language = request.POST.get('to', "id")
        dataresponse = translater(language,values,values)
        data = {
            "data": dataresponse or "Not found text"
        }
        return JsonResponse(data)

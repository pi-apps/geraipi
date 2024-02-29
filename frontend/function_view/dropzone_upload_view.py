from .base_view import FrontPage
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class UploadDropzone(FrontPage):
    def get(self, request):
        return JsonResponse({"status": True, "uuid": "1"})

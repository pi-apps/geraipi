from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_required, name="dispatch")
class TokenView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.fcm_token = request.POST.get("fcm_token")
        user.save()
        if user.fcm_token:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})

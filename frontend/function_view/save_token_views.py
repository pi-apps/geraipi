from .base_view import FrontPage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from profiles.models import UserProfile
from django.http import JsonResponse


@method_decorator(csrf_exempt, name='dispatch')
class SaveToken(FrontPage):
    def get(self, request):
        accesstoken = request.POST.get("accessToken", None)
        backendurl = request.POST.get("backendURL", None)
        frontendurl = request.POST.get("frontendURL", None)
        response = { "success": True }
        if accesstoken and backendurl and frontendurl :
            users = UserProfile.objects.get(username=request.user)
            user_profile = UserProfile.objects.get(users=users)
            user_profile.token_backend = accesstoken
            user_profile.url_backend = backendurl
            user_profile.url_frontend = frontendurl
            user_profile.save()
            print(user_profile)
            response = { "success": True }
        return JsonResponse(response)
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from profiles.models import UserProfile, UserProfileAddress

from .base_view import FrontPage


@method_decorator(csrf_exempt, name="dispatch")
class DetailProfileAddressMain(FrontPage):
    def post(self, request, id):
        userss = UserProfile.objects.get(users_id=request.user.id)
        data = {"status": False}
        try:
            usernames = UserProfileAddress.objects.get(userprofile_id=userss.pk, pk=id)
            usernames.is_primary = True
            usernames.save()
            useraddress2 = UserProfileAddress.objects.filter(userprofile_id=userss.pk).exclude(id=id)
            for useraddresss in useraddress2:
                useraddresss.is_primary = False
                useraddresss.save()
            data = {"status": True}
        except UserProfile.DoesNotExist:
            data = {"status": False}
        return JsonResponse(data)

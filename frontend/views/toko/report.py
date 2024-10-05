from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from frontend.views.base_view import FrontPage
from store.models import UserStore
from transaction.models import Report, ReportImage


@method_decorator(csrf_exempt, name="dispatch")
class ReportToko(FrontPage):
    def get(self, request, id):
        user_setting = request.user.id
        user_toko = request.user.userstore_set.first()
        return render(request, "toko/report.html", {"user_toko": user_toko})

    def post(self, request, id):
        user = UserStore.objects.filter(users_id=id).first()
        if user is None:
            user = UserStore.objects.create(users_id=id)
        if request.POST.get("setuju"):
            user.aggrement = True
        else:
            user.aggrement = False
        user.save()
        return redirect("/toko/" + str(id))

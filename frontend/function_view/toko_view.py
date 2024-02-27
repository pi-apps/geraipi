from .base_view import FrontPage
from django.shortcuts import render, redirect
from store.models import UserStore
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class Toko(FrontPage):
    def get(self,request,id):
        user = UserStore.objects.filter(users_id=id).first()
        if request.method == "POST":
            if user is None:
                user = UserStore.objects.create(users_id=id)
            if request.POST.get("setuju"):
                user.aggrement = True
            else:
                user.aggrement = False
            user.save()
        return render(request, 'toko/toko_profile.html',{"user_toko": user })
    
    def post(self, request, id):
        user = UserStore.objects.filter(users_id=id).first()
        if user is None:
            user = UserStore.objects.create(users_id=id)
        if request.POST.get("setuju"):
            user.aggrement = True
        else:
            user.aggrement = False
        user.save()
        return redirect('/toko/'+str(id))

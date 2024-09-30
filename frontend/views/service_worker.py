from django.shortcuts import render
from django.views import View


class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "firebase-messaging-sw.js", content_type="application/x-javascript")

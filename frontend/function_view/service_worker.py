from django.views import View
from django.shortcuts import render

class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'firebase-messaging-sw.js', content_type="application/x-javascript")
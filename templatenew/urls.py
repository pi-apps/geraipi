from django.urls import path

from .views.fcm.token_view import TokenView
from .views.home.index import Home

urlpatterns = [
    path("", Home.as_view()),
    path("fcm-token", TokenView.as_view(), name="fcm_token"),
]

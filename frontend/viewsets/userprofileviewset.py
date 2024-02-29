from rest_framework import viewsets

from frontend.serializers import UserProfileSerializer
from profiles.models import UserProfile


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

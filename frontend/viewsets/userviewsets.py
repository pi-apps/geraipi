from frontend import viewsets
from frontend.serializers import UserSerializer
from profiles.models import UserProfile


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

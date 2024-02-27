from django.contrib.auth.models import Group
from rest_framework import generics, permissions, views, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apidata.serializers.auth_serializer import (GroupSerializer, MeSerializer,
                                                 RegisterSerializer,
                                                 UserSerializer)
from profiles.models import UserProfile


class UserAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        datas = request.data
        datas["password"] = datas["username"]
        serializer = self.serializer_class(data=datas, context={"request": request})
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "success": True,
                    "token": token.key,
                    "user_id": user.pk,
                    "email": user.email,
                }
            )
        else:
            user = None
            try:
                user = UserProfile.objects.get(username=datas["username"])
            except UserProfile.DoesNotExist:
                user = UserProfile.objects.create(username=datas["username"])
            user.is_staff = True
            user.set_password(datas["password"])
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "success": True,
                    "token": token.key,
                    "user_id": user.pk,
                    "email": user.email,
                }
            )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    authentication_classes = [TokenAuthentication]
    queryset = UserProfile.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user:
    #         queryset = queryset.filter(pk=self.request.user.id)
    #     return queryset


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MeViewSet(views.APIView):
    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        usernames = request.user
        usernames = MeSerializer(usernames).data
        return Response(usernames)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

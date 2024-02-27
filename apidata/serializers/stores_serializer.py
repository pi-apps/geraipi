from rest_framework import serializers

from apidata.serializers.auth_serializer import UserSerializer
# from django.contrib.auth.models import User
from profiles.models import UserProfile
from store.models import UserNotification, UserStore, UserStoreAddress


class UserStoreSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    class Meta:
        model = UserStore
        fields = ["nama", "deskripsi", "id"]

    # def get_user(self, obj):
    #     user = UserProfile.objects.filter(pk=obj.users.id)
    #     return UserSerializer(user, many=True).data


class UserStoreAddressSerializer(serializers.ModelSerializer):
    userstore = UserStoreSerializer(many=True)

    class Meta:
        model = UserStoreAddress
        fields = ["address"]

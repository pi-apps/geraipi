# from django.contrib.auth.models import User
from rest_framework import serializers

from store.models import UserStore, UserStoreAddress


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

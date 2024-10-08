from django.contrib.auth.models import Group
from profiles.models import UserProfile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'nama', 'no_telepon', 'id']


class MeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'coin', 'id',  'nama', 'no_telepon']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(required=True)
    token = serializers.SerializerMethodField()
    # password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'token')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        user = UserProfile.objects.create(
            username=validated_data['username'],
            is_staff=True,
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.serializers import ModelSerializer, CharField


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'password', 'likes', 'conversations']


class CreateUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'password']

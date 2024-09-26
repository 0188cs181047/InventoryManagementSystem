from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import IMSUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=IMSUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_enterpass = serializers.CharField(write_only=True, required=True)
    is_staff = serializers.BooleanField(default=False)  # Added field
    is_superuser = serializers.BooleanField(default=False)  # Added field

    class Meta:
        model = IMSUser
        fields = ('username', 'email', 'password', 're_enterpass', 'is_staff', 'is_superuser')

    def validate(self, attrs):
        if attrs['password'] != attrs['re_enterpass']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = IMSUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

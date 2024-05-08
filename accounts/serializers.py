from django.forms import ValidationError
from .models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=8, write_only=True)

    
    class Meta:
        model = User
        fields = ["email", "username", "password"]


    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("Email is already in use")

        return super().validate(attrs)
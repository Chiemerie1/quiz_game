from django.forms import ValidationError
from .models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


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
        
        if User.objects.filter(username=attrs["username"]).exists():
            raise ValidationError("username has already been taken")

        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        ### creating token for the user
        Token.objects.create(user=user)
        return user
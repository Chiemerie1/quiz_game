from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# Create your views here.



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Successfully created",
                "data": data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = []
    def post(self, request: Request):
        email =  request.data["email"]
        password = request.data["password"]

        user = authenticate(email=email, password=password)
        if user is not None:
            response = {
                "message": f'{str(user)} authenticated',
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data={"message": "Wrong credentials"})

    def get(self, request: Request):
        user = request.user
        response = {
            "user": str(user),
            "auth": str(request.auth)
        }
        return Response(data=response, status=status.HTTP_200_OK)
    

from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .serializers import ContestSerializer, QuestionAndOptionsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from .models import Contest, QuestionAndOptions, UserParticipation, LeaderBoard
from .serializers import ContestSerializer, QuestionAndOptionsSerializer

# Create your views here.



@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def contest_list(request: Request):
    contest = Contest.objects.all()

    if request.method == "POST":
        data = request.data
        serializer = ContestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            response = {
                "message": "Created",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == "GET":
        serializer = ContestSerializer(instance=contest, many=True)
        response = {
            "message": "contest",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_contest_detail(request: Request, contest_id: int):
    contest = get_object_or_404(Contest, pk=contest_id)

    serializer =  ContestSerializer(instance=contest)
    response = {
        "message": "contest_detail",
        "data": serializer.data
    }

    return Response(data=response, status=status.HTTP_200_OK)



@api_view(http_method_names=["PUT"])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_contest(request: Request, contest_id: int):
    contest = get_object_or_404(Contest, pk=contest_id)

    data = request.data

    serializer =  ContestSerializer(instance=contest, data=data)
    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Updated",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=["DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_contest(request: Request, contest_id: int):
    contest = get_object_or_404(Contest, pk=contest_id)
    contest.delete()
    return Response(data={"message": "Contest deleted"}, status=status.HTTP_204_NO_CONTENT)
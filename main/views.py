
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .serializers import ContestSerializer, QuestionAndOptionsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .models import Contest, QuestionAndOptions, UserParticipation, LeaderBoard
from .serializers import ContestSerializer, QuestionAndOptionsSerializer, AnswerSerializer
# for cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from drf_spectacular.utils import extend_schema




# Create your views here.


@cache_page(60* 60 * 3)
@extend_schema(request=ContestSerializer, responses=ContestSerializer)
@method_decorator(vary_on_headers("Authorization"))
@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAdminUser])
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
    

    elif request.method == "GET":
        serializer = ContestSerializer(instance=contest, many=True)
        response = {
            "message": "contest",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@cache_page(60* 60 * 3)
@extend_schema(request=None, responses=ContestSerializer)
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_contest_list(request: Request):
    contest = Contest.objects.all()    
    serializer = ContestSerializer(instance=contest, many=True)
    response = {
        "message": "contest",
        "data": serializer.data
    }
    return Response(data=response, status=status.HTTP_200_OK)


@extend_schema(request=ContestSerializer, responses=ContestSerializer)
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


@extend_schema(request=ContestSerializer, responses=ContestSerializer)
@api_view(http_method_names=["PUT"])
@permission_classes([IsAdminUser])
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



@extend_schema(request=None, responses=None)
@api_view(http_method_names=["DELETE"])
@permission_classes([IsAdminUser])
def delete_contest(request: Request, contest_id: int):
    contest = get_object_or_404(Contest, pk=contest_id)
    contest.delete()
    return Response(data={"message": "Contest deleted"}, status=status.HTTP_204_NO_CONTENT)



@extend_schema(request=QuestionAndOptionsSerializer, responses=None)
@api_view(http_method_names=["POST"])
@permission_classes([IsAdminUser])
def add_question(request: Request):
    data = request.data
    serializer = QuestionAndOptionsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    
        response = {
            "message": "Posted",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@extend_schema(request=None, responses=QuestionAndOptionsSerializer)
@cache_page(60* 60 * 3)
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_quiz(request: Request):
    questions = QuestionAndOptions().get_shuffled_questions()
    
    serializer = QuestionAndOptionsSerializer(instance=questions, many=True)
    
    response = {
        "message": "Retrieved",
        "data": serializer.data
    }
    return Response(data=response, status=status.HTTP_200_OK)
    



@cache_page(60* 60 * 3)
@extend_schema(request=AnswerSerializer, responses=None)
@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def quiz_functions(request: Request, question_id: int, contest_id: int):

    contest = Contest.objects.get(pk=contest_id)
    user_weekly_score = LeaderBoard().compute_weekly_score(request.user.id)
    leader_board, _ = LeaderBoard.objects.get_or_create(user=request.user, contest=contest)
    leader_board.weekly_score = user_weekly_score["total_score"]
    leader_board.save()
    

    user_participation, _ = UserParticipation.objects.get_or_create(contest=contest_id, user=request.user.id)
    question = get_object_or_404(QuestionAndOptions, pk=question_id)
    data = request.data
    if question.answer == data["select_choice"]:
        user_participation.score += 2
        user_participation.save()

        response = {
            "message": "correct answer",
            "current score": user_participation.score
        }
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(data={"message": "Failed"}, status=status.HTTP_200_OK)


### Database indexing:      check
### Efficiency in querries: check
### Caching:                check
### Asynchronous Processing:


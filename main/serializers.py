
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Contest, QuestionAndOptions, UserParticipation, LeaderBoard



class ContestSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=100)
    class Meta:
        model = Contest
        fields = ["id", "title", "description", "end_date"]



class QuestionAndOptionsSerializer(serializers.ModelSerializer):

    answer = serializers.CharField(max_length=100, required=True)
    option1 = serializers.CharField(max_length=100, required=True)
    option2 = serializers.CharField(max_length=100, required=True)
    option3 = serializers.CharField(max_length=100, required=True)
    option4 = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = QuestionAndOptions
        fields = ["__all__"]





from django.db import models
from accounts.models import User
from django.db.models import Sum

# Create your models here.



class Contest(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_ongoing = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    


class QuestionAndOptions(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)

    def get_shuffled_questions(self):
        self.shuffled_queryset = QuestionAndOptions.objects.raw(
            'SELECT * FROM main_questionandoptions ORDER BY RANDOM()'
        )
        return self.shuffled_queryset
    
    

    def __str__(self) -> str:
        return f'{str(self.contest.title)} question'
    


class UserParticipation(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.user.username} - {self.contest.title} - Score: {self.score}"



class LeaderBoard(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekly_rank = models.IntegerField(default=0)
    weekly_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["-weekly_score"]

    ### remember to aggregate for all quiz score for weekly scores
    def compute_weekly_score(self, user_id: int):
        # total_score = 0
        self.this_user_score = UserParticipation.objects.filter(user=user_id)
        self.this_user_score = self.this_user_score.aggregate(total_score=Sum("score"))
        return self.this_user_score
        # self.this_user_score.values("score").all()
        # for score in self.this_user_score:
        #     total_score += score.score

    def __str__(self) -> str:
        return f"{self.user.username} - Contest: {self.contest.title} - Weekly Score: {self.weekly_score}"
    


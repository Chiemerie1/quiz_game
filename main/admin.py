from django.contrib import admin
from .models import QuestionAndOptions, Contest, LeaderBoard, UserParticipation

# Register your models here.


class ContestAdmin(admin.ModelAdmin):
    list_display = ["title", "start_date", "end_date", "is_ongoing"]

admin.site.register(Contest, ContestAdmin)


class QuestionAndOptionsAdmin(admin.ModelAdmin):
    list_display = ["contest", "answer"]

admin.site.register(QuestionAndOptions, QuestionAndOptionsAdmin)


class UserParticipationAdmin(admin.ModelAdmin):
    list_display = ["contest", "user", "score"]

admin.site.register(UserParticipation, UserParticipationAdmin)


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ["contest", "user", "weekly_rank", "weekly_score"]

admin.site.register(LeaderBoard, LeaderBoardAdmin)



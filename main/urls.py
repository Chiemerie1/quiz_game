from django.urls import path
from . import views



app_name = "accounts"

urlpatterns = [
    path("api/create-contest/", views.contest_list, name="create_contest"),
    path("api/get-contest/<int:contest_id>/", views.get_contest_detail, name="contest_detail")

]

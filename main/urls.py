from django.urls import path
from . import views



app_name = "main"

urlpatterns = [
    path("api/create-contest/", views.contest_list, name="create_contest"),
    path("api/get-contest/", views.get_contest_list, name="get_contest"),
    path("api/get-contest/<int:contest_id>/", views.get_contest_detail, name="contest_detail"),
    path("api/update-contest/<int:contest_id>", views.update_contest, name="update_detail"),
    path("api/delete-contest/<int:contest_id>/", views.delete_contest, name="delete_detail"),

]

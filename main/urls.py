from django.urls import path
from . import views

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi





schema_view = get_schema_view(
   openapi.Info(
      title="Quiz Game API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="chiemeriedroid@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


app_name = "main"

urlpatterns = [
    path("api/create-contest/", views.contest_list, name="create_contest"),
    path("api/get-contest/", views.get_contest_list, name="get_contest"),
    path("api/get-contest/<int:contest_id>/", views.get_contest_detail, name="contest_detail"),
    path("api/update-contest/<int:contest_id>", views.update_contest, name="update_detail"),
    path("api/delete-contest/<int:contest_id>/", views.delete_contest, name="delete_detail"),
    path("api/create-question/", views.quiz, name="create_questions"),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

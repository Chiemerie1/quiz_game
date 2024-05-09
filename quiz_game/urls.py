
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView







urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("auth/", include("accounts.urls")),
    path('api/jwt/token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

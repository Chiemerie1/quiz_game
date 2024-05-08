from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import User


user = get_user_model()


def create_jwt_user_tokens(user: User):
    refresh_token = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh_token.access_token),
        "refresh": str(refresh_token)
    }
    return tokens
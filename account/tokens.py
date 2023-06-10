from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

def create_token(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        "id": str(user.id),
        "email": user.email,
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
    return tokens
# users/urls.py
from django.urls import path
from .views import UserCreateView
from rest_framework.authtoken.views import obtain_auth_token # Import this

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', obtain_auth_token, name='api-token-auth'), # Add this line
]
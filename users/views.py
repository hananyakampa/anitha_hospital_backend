# users/views.py
from rest_framework import generics, permissions
from .serializers import UserCreationSerializer
from .models import User # Import User model

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # We'll secure this later
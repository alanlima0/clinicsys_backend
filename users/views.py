# users/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)
from .permissions import IsAdminClinica

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminClinica]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserMeSerializer
)
from .permissions import IsAdminClinica

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAuthenticated, IsAdminClinica]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user.id == self.get_object().id:
            return Response(
                {"detail": "Você não pode excluir seu próprio usuário"},
                status=400
            )
        return super().destroy(request, *args, **kwargs)
    

      # 🔐 LOGOUT
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logout realizado com sucesso"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Refresh token inválido ou ausente"},
                status=status.HTTP_400_BAD_REQUEST
            )
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
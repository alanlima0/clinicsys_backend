from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.permissions import PacientePermission, IsAdminClinica

from .models import Paciente
from .serializers import PacienteSerializer


class PacienteViewSet(ModelViewSet):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Paciente.objects.all().order_by('-data_cadastro')

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(nome__icontains=search))
        return queryset
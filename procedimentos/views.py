from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Procedimento
from .serializers import ProcedimentoSerializer


class ProcedimentoViewSet(ModelViewSet):
    
    serializer_class = ProcedimentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Procedimento.objects.all().order_by('nome')

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(nome__icontains=search))
        return queryset
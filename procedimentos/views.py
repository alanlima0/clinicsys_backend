from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Procedimento
from .serializers import ProcedimentoSerializer


class ProcedimentoViewSet(ModelViewSet):
    queryset = Procedimento.objects.all().order_by('nome')
    serializer_class = ProcedimentoSerializer
    permission_classes = [IsAuthenticated]

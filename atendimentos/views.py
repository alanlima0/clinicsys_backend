from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Atendimento,
    Triagem, Anamnese, Prescricao
)
from .serializers import *

from caixa.serializers import CaixaDiarioSerializer
from caixa.models import CaixaDiario


# class AtendimentoViewSet(viewsets.ModelViewSet):
#     queryset = Atendimento.objects.all()
    
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return AtendimentoCreateSerializer
#         elif self.action == 'retrieve':
#             return AtendimentoDetalheSerializer
#         return AtendimentoListSerializer

class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AtendimentoCreateSerializer
        elif self.action == 'retrieve':
            return AtendimentoDetalheSerializer
        return AtendimentoListSerializer

    def get_queryset(self):
        # 1. Pega a queryset padrão (Atendimento.objects.all())
        queryset = super().get_queryset()
        
        # 2. Verifica se existe o parâmetro '?data=YYYY-MM-DD' na URL
        data_filtro = self.request.query_params.get('data', None)
        
        if data_filtro:
            # 3. Aplica o filtro
            # ⚠️ ATENÇÃO: Estou a usar 'criado_em__date'. 
            # Se o campo de data no seu model Atendimento se chamar de outra forma 
            # (ex: 'data_atendimento'), mude 'criado_em__date' para 'data_atendimento__date'.
            queryset = queryset.filter(criado_em__date=data_filtro)
            
        return queryset
    
    # 📋 ROTA: Listar fila de atendimentos
    @action(detail=False, methods=['get'], url_path='fila')
    def fila(self, request):
        """
        GET /api/atendimentos/fila/
        Retorna atendimentos não finalizados, ordenados por prioridade
        """
        atendimentos = Atendimento.objects.filter(
            finalizado=False
        ).order_by(
            '-prioridade',
            'criado_em'
        )
        serializer = self.get_serializer(atendimentos, many=True)
        return Response(serializer.data)
    
    # 🔔 ROTA: Chamar atendimento
    @action(detail=True, methods=['post'], url_path='chamar')
    def chamar(self, request, pk=None):
        """
        POST /api/atendimentos/{id}/chamar/
        Marca atendimento como chamado
        """
        atendimento = self.get_object()
        atendimento.chamado = True
        atendimento.save()
        serializer = self.get_serializer(atendimento)
        return Response(serializer.data)
    
    # ✅ ROTA: Finalizar atendimento
    @action(detail=True, methods=['post'], url_path='finalizar')
    def finalizar(self, request, pk=None):
        """
        POST /api/atendimentos/{id}/finalizar/
        Marca atendimento como finalizado
        """
        atendimento = self.get_object()
        atendimento.finalizado = True
        atendimento.save()
        serializer = self.get_serializer(atendimento)
        return Response(serializer.data)
    
    # 📊 ROTA: Prontuário completo
    @action(detail=True, methods=['get'], url_path='prontuario')
    def prontuario(self, request, pk=None):
        """
        GET /api/atendimentos/{id}/prontuario/
        Retorna todos os dados do atendimento (triagem, anamnese, prescrições)
        """
        atendimento = self.get_object()
        serializer = AtendimentoDetalheSerializer(atendimento)
        return Response(serializer.data)

    # 🩺 ROTA: Buscar triagem pelo atendimento
    @action(detail=True, methods=['get'], url_path='triagem')
    def triagem(self, request, pk=None):
        """
        GET /api/atendimentos/{id}/triagem/
        """
        atendimento = self.get_object()
        triagem = Triagem.objects.filter(atendimento=atendimento).first()

        if not triagem:
            return Response(
                {"detail": "Triagem não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TriagemSerializer(triagem)
        return Response(serializer.data)

    # 📋 ROTA: Buscar anamnese pelo atendimento
    @action(detail=True, methods=['get'], url_path='anamnese')
    def anamnese(self, request, pk=None):
        """
        GET /api/atendimentos/{id}/anamnese/
        """
        atendimento = self.get_object()
        anamnese = Anamnese.objects.filter(atendimento=atendimento).first()

        if not anamnese:
            return Response(
                {"detail": "Anamnese não encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AnamneseSerializer(anamnese)
        return Response(serializer.data)

    # 💊 ROTA: Buscar prescrições pelo atendimento
    @action(detail=True, methods=['get'], url_path='prescricoes')
    def prescricoes(self, request, pk=None):
        """
        GET /api/atendimentos/{id}/prescricoes/
        """
        atendimento = self.get_object()
        prescricoes = Prescricao.objects.filter(atendimento=atendimento)

        serializer = PrescricaoSerializer(prescricoes, many=True)
        return Response(serializer.data)


class TriagemViewSet(viewsets.ModelViewSet):
    """
    POST /api/triagens/
    Body: { "atendimento": 1, "peso": 70.5, "altura": 1.75, ... }
    """
    queryset = Triagem.objects.all()
    serializer_class = TriagemSerializer


class AnamneseViewSet(viewsets.ModelViewSet):
    """
    POST /api/anamneses/
    Body: { "atendimento": 1, "queixa_principal": "..." }
    """
    queryset = Anamnese.objects.all()
    serializer_class = AnamneseSerializer


class PrescricaoViewSet(viewsets.ModelViewSet):
    """
    POST /api/prescricoes/
    Body: { "atendimento": 1, "descricao": "..." }
    """
    queryset = Prescricao.objects.all()
    serializer_class = PrescricaoSerializer


class CaixaDiarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Apenas leitura - registro é criado automaticamente
    """
    queryset = CaixaDiario.objects.all()
    serializer_class = CaixaDiarioSerializer
    
    @action(detail=False, methods=['get'], url_path='hoje')
    def hoje(self, request):
        """
        GET /api/caixa-diario/hoje/
        Retorna registros de hoje
        """
        from django.utils import timezone
        hoje = timezone.now().date()
        registros = CaixaDiario.objects.filter(
            criado_em__date=hoje
        )
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='relatorio')
    def relatorio(self, request):
        """
        GET /api/caixa-diario/relatorio/?data_inicio=2026-01-01&data_fim=2026-01-31
        Relatório por período
        """
        from django.db.models import Sum
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        queryset = CaixaDiario.objects.all()
        
        if data_inicio:
            queryset = queryset.filter(criado_em__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado_em__date__lte=data_fim)
        
        totais = queryset.values('forma_pagamento').annotate(
            total=Sum('valor')
        )
        
        return Response({
            'registros': self.get_serializer(queryset, many=True).data,
            'total_geral': queryset.aggregate(Sum('valor'))['valor__sum'] or 0,
            'totais_por_forma': list(totais)
        })
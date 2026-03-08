from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone # ✅ IMPORTAÇÃO ADICIONADA AQUI

from .models import Atendimento, Triagem, Anamnese, Prescricao
from .serializers import *

from caixa.serializers import CaixaDiarioSerializer
from caixa.models import CaixaDiario


class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AtendimentoCreateSerializer
        elif self.action == 'retrieve':
            return AtendimentoDetalheSerializer
        return AtendimentoListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        data_filtro = self.request.query_params.get('data')

        if data_filtro:
            queryset = queryset.filter(criado_em__date=data_filtro)

        return queryset

    # 📋 FILA DE ATENDIMENTO
    @action(detail=False, methods=['get'], url_path='fila')
    def fila(self, request):
        atendimentos = Atendimento.objects.filter(
            finalizado=False
        ).order_by(
            '-chamado',      # chamados aparecem primeiro
            '-prioridade',   # depois prioridade
            'criado_em'      # depois ordem de chegada
        )

        serializer = self.get_serializer(atendimentos, many=True)
        return Response(serializer.data)

    # 🔔 CHAMAR PACIENTE (ATUALIZADO PARA MÚLTIPLOS PROCEDIMENTOS E CHAMADAS REPETIDAS)
    @action(detail=True, methods=['post'], url_path='chamar')
    def chamar(self, request, pk=None):
        atendimento = self.get_object()

        if atendimento.finalizado:
            return Response(
                {"erro": "Atendimento já finalizado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ✅ Agora ele atualiza também a 'hora_chamada' com o momento exato do clique
        Atendimento.objects.filter(
            paciente=atendimento.paciente,
            criado_em__date=atendimento.criado_em.date(),
            finalizado=False
        ).update(chamado=True, hora_chamada=timezone.now())

        # Atualiza o objeto atual com as informações novas do banco
        atendimento.refresh_from_db()

        serializer = self.get_serializer(atendimento)
        return Response(serializer.data)

    # ✅ FINALIZAR ATENDIMENTO (ATUALIZADO PARA MÚLTIPLOS PROCEDIMENTOS)
    @action(detail=True, methods=['post'], url_path='finalizar')
    def finalizar(self, request, pk=None):
        atendimento = self.get_object()

        if not atendimento.chamado:
            return Response(
                {"erro": "Paciente ainda não foi chamado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if atendimento.finalizado:
            return Response(
                {"erro": "Atendimento já finalizado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Encontra e marca como FINALIZADO todos os procedimentos 
        # desse mesmo paciente na data de hoje
        Atendimento.objects.filter(
            paciente=atendimento.paciente,
            criado_em__date=atendimento.criado_em.date(),
            finalizado=False
        ).update(finalizado=True)

        # Atualiza o objeto atual com as informações novas do banco
        atendimento.refresh_from_db()

        serializer = self.get_serializer(atendimento)
        return Response(serializer.data)

    # 📺 ÚLTIMO PACIENTE CHAMADO (PAINEL DA TV)
    @action(detail=False, methods=['get'], url_path='ultimo-chamado', permission_classes=[AllowAny])
    def ultimo_chamado(self, request):
        atendimento = Atendimento.objects.filter(
            chamado=True,
            finalizado=False
        ).order_by('-hora_chamada').first()

        if not atendimento:
            return Response({"paciente": None})

        data = self.get_serializer(atendimento).data
        data['hora_chamada'] = atendimento.hora_chamada
        
        return Response(data)

    # 📊 PRONTUÁRIO COMPLETO
    @action(detail=True, methods=['get'], url_path='prontuario')
    def prontuario(self, request, pk=None):
        atendimento = self.get_object()
        serializer = AtendimentoDetalheSerializer(atendimento)
        return Response(serializer.data)

    # 📂 HISTÓRICO DO PACIENTE
    @action(detail=True, methods=['get'], url_path='historico')
    def historico(self, request, pk=None):
        atendimento_atual = self.get_object()
        
        # Busca todos os atendimentos deste paciente (incluindo o atual), do mais recente ao mais antigo
        historicos = Atendimento.objects.filter(
            paciente=atendimento_atual.paciente
        ).order_by('-criado_em')

        serializer = AtendimentoListSerializer(historicos, many=True)
        return Response(serializer.data)

    # 🩺 TRIAGEM
    @action(detail=True, methods=['get'], url_path='triagem')
    def triagem(self, request, pk=None):
        atendimento = self.get_object()
        triagem = Triagem.objects.filter(atendimento=atendimento).first()

        if not triagem:
            return Response({"detail": "Triagem não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TriagemSerializer(triagem)
        return Response(serializer.data)

    # 📋 ANAMNESE
    @action(detail=True, methods=['get', 'post'], url_path='anamnese')
    def anamnese(self, request, pk=None):
        atendimento = self.get_object()

        if request.method == 'GET':
            anamnese = Anamnese.objects.filter(atendimento=atendimento).first()
            if not anamnese:
                return Response({"detail": "Anamnese não encontrada"}, status=status.HTTP_404_NOT_FOUND)
            serializer = AnamneseSerializer(anamnese)
            return Response(serializer.data)

        # POST: Cria ou Atualiza a Anamnese
        queixa_principal = request.data.get('queixa_principal', '')
        anamnese, created = Anamnese.objects.update_or_create(
            atendimento=atendimento,
            defaults={'queixa_principal': queixa_principal}
        )
        return Response(AnamneseSerializer(anamnese).data, status=status.HTTP_200_OK)

    # 💊 PRESCRIÇÕES
    @action(detail=True, methods=['get', 'post'], url_path='prescricoes')
    def prescricoes(self, request, pk=None):
        atendimento = self.get_object()

        if request.method == 'GET':
            prescricoes = Prescricao.objects.filter(atendimento=atendimento)
            serializer = PrescricaoSerializer(prescricoes, many=True)
            return Response(serializer.data)

        # POST: Cria ou Atualiza a Prescrição principal
        descricao = request.data.get('descricao', '')
        if descricao:
            prescricao = Prescricao.objects.filter(atendimento=atendimento).first()
            if prescricao:
                prescricao.descricao = descricao
                prescricao.save()
            else:
                prescricao = Prescricao.objects.create(atendimento=atendimento, descricao=descricao)
            return Response(PrescricaoSerializer(prescricao).data, status=status.HTTP_200_OK)
            
        return Response({"erro": "A descrição não pode estar vazia"}, status=status.HTTP_400_BAD_REQUEST)


class TriagemViewSet(viewsets.ModelViewSet):
    queryset = Triagem.objects.all()
    serializer_class = TriagemSerializer


class AnamneseViewSet(viewsets.ModelViewSet):
    queryset = Anamnese.objects.all()
    serializer_class = AnamneseSerializer


class PrescricaoViewSet(viewsets.ModelViewSet):
    queryset = Prescricao.objects.all()
    serializer_class = PrescricaoSerializer


class CaixaDiarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CaixaDiario.objects.all()
    serializer_class = CaixaDiarioSerializer

    @action(detail=False, methods=['get'], url_path='hoje')
    def hoje(self, request):
        from django.utils import timezone
        hoje = timezone.now().date()
        registros = CaixaDiario.objects.filter(criado_em__date=hoje)
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='relatorio')
    def relatorio(self, request):
        from django.db.models import Sum
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        queryset = CaixaDiario.objects.all()

        if data_inicio:
            queryset = queryset.filter(criado_em__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado_em__date__lte=data_fim)

        totais = queryset.values('forma_pagamento').annotate(total=Sum('valor'))

        return Response({
            'registros': self.get_serializer(queryset, many=True).data,
            'total_geral': queryset.aggregate(Sum('valor'))['valor__sum'] or 0,
            'totais_por_forma': list(totais)
        })
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AtendimentoViewSet,
    TriagemViewSet, 
    AnamneseViewSet, 
    PrescricaoViewSet,
    CaixaDiarioViewSet
)

router = DefaultRouter()
router.register(r'atendimentos', AtendimentoViewSet, basename='atendimento')
router.register(r'triagens', TriagemViewSet, basename='triagem')
router.register(r'anamneses', AnamneseViewSet, basename='anamnese')
router.register(r'prescricoes', PrescricaoViewSet, basename='prescricao')
router.register(r'caixa-diario', CaixaDiarioViewSet, basename='caixa-diario')

urlpatterns = [
    path('', include(router.urls)),
]
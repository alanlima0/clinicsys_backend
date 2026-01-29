from rest_framework.routers import DefaultRouter
from .views import ProcedimentoViewSet

router = DefaultRouter()
router.register(r'procedimentos', ProcedimentoViewSet, basename='procedimentos')

urlpatterns = router.urls

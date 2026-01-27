from django.urls import path
from .views import TesteJWTView

urlpatterns = [
    path('teste/', TesteJWTView.as_view(), name='teste-jwt'),
]

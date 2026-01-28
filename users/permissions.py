from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsAdminClinica(BasePermission):
    """
    Permite acesso apenas a usuários ADMIN
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.tipo_usuario == 'ADMIN'
        )


class PacientePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.tipo_usuario == 'RECEPCAO':
            return True

        if request.user.tipo_usuario == 'MEDICO' and request.method in SAFE_METHODS:
            return True

        return False

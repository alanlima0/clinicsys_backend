from rest_framework.permissions import BasePermission

class IsAdminClinica(BasePermission):
    """
    Permite acesso apenas a usuários ADMIN
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.tipo_usuario == 'ADMIN'
        )

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'tipo_usuario', 'is_active')
    search_fields = ('email', 'nome')

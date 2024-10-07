from django.contrib import admin
from .models import Task
from rest_framework.authtoken.models import Token

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Campos a mostrar en la lista
    search_fields = ('title',)  # Campos por los que se puede buscar
    ordering = ('created_at',)  # Ordenar por fecha de creación


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created')
    search_fields = ('user__username', 'key')



# Registramos nuevamente el Token con nuestra configuración personalizada
admin.site.register(Token, TokenAdmin)


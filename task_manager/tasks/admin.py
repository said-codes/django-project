from django.contrib import admin
from rest_framework.authtoken.models import  TokenProxy
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Campos a mostrar en la lista
    search_fields = ('title',)  # Campos por los que se puede buscar
    ordering = ('created_at',)  # Ordenar por fecha de creación


# Desregistrar TokenProxy si está registrado
try:
    admin.site.unregister(TokenProxy)
except admin.sites.NotRegistered:
    pass


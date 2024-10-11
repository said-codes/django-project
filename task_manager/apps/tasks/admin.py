from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', "enabled")  # Campos a mostrar en la lista
    search_fields = ('title',)  # Campos por los que se puede buscar
    ordering = ('created_at',)  # Ordenar por fecha de creación



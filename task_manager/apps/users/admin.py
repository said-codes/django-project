from django.contrib import admin
from .models import User

# Register your models here.
from django.contrib import admin
from .models import User

# Registro del modelo User en el admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'email','photo', 'phone', 'created_at')  # Campos que se mostrarán en la lista
    search_fields = ('name', 'lastname', 'email')  # Campos que puedes buscar
    list_filter = ('created_at', 'updated_at')  # Filtros para la barra lateral

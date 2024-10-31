from django.contrib import admin
from apps.users.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Registro del modelo User en el admin

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created', 'modified', 'enable')  # Campos que se mostrarán en la lista
    search_fields = ('name','email')  # Campos que puedes buscar

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'email','avatar', 'phone', 'created','get_token')  # Campos que se mostrarán en la lista
    search_fields = ('name', 'lastname', 'email')  # Campos que puedes buscar
    list_filter = ('created', 'modified')  # Filtros para la barra lateral

    def get_token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return 'No Token'

    get_token.short_description = 'Token'  # Nombre de la columna en el admin



User = get_user_model()

admin.site.register(Customer, CustomerAdmin)
admin.site.register(User, UserAdmin)

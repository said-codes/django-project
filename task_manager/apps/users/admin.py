from django.contrib import admin
from apps.users.models import *

# Registro del modelo User en el admin

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created', 'modified', 'enable')  # Campos que se mostrarán en la lista
    search_fields = ('name', 'email')  # Campos que puedes buscar

admin.site.register(Customer, CustomerAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'email','avatar', 'phone', 'created')  # Campos que se mostrarán en la lista
    search_fields = ('name', 'lastname', 'email')  # Campos que puedes buscar
    list_filter = ('created', 'modified')  # Filtros para la barra lateral
admin.site.register(User, UserAdmin)

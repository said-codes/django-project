from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # Nuevo campo para registrar el tiempo de finalización

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()  # Asignar el momento actual al completar la tarea
        super().save(*args, **kwargs)

    def duration(self):
        if self.completed and self.completed_at:
            return self.completed_at - self.created_at  # Devuelve la duración en timedelta
        return None


    def __str__(self):
        return self.title


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created')
    search_fields = ('user__username', 'key')

admin.site.register(Token, TokenAdmin)

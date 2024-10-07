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


    @property
    def duration(self):
        if self.completed_at:
            duration_seconds = (self.completed_at - self.created_at).total_seconds()
            return duration_seconds
        return None

    def formatted_duration(self):
        if self.duration is not None:
            days = int(self.duration // (24 * 3600))
            hours = int((self.duration % (24 * 3600)) // 3600)
            minutes = int((self.duration % 3600) // 60)
            seconds = int(self.duration % 60)
            duration_parts = []
            if days > 0:
                duration_parts.append(f"{days} días")
            if hours > 0:
                duration_parts.append(f"{hours} horas")
            if minutes > 0:
                duration_parts.append(f"{minutes} minutos")
            if seconds > 0:
                duration_parts.append(f"{seconds} segundos")
            return ', '.join(duration_parts)
        return "No disponible"



    def __str__(self):
        return self.title



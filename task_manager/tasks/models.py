from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created')
    search_fields = ('user__username', 'key')

admin.site.register(Token, TokenAdmin)

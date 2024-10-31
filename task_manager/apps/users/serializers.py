from rest_framework import serializers
from apps.tasks.models import Task
from apps.users.models import User, Customer
from django.contrib.auth import password_validation, authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','lastname','document','email','phone','avatar','enabled','groups']

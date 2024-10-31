from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import TaskSerializer, UserSerializer, CustomerSerializer
from apps.tasks.models import Task
from apps.users.models import User, Customer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from apps.api.serializers import *
from dateutil import tz
from datetime import datetime
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework import status
from .serializers import GroupSerializer  # Asegúrate de tener un serializador definido
# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happeni


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['post'])
    def login(self, request):
        # print("login UserViewSet", request.data)
        serializer = UserLoginSerializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        colombia = tz.gettz('America/Bogota')
        user.last_login = datetime.now(colombia)
        # user.save()
        # groups_name=str(user.groups.all()[0])
        User.objects.filter(id=user.id).update(
            last_login=datetime.now(colombia))
        data = {
            "user": UserSerializer(user).data,
            "access_token": token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])  # REGISTRO DE USUARIOS
    def signup(self, request):
        if request.data['avatar']:  # si viene con foto llama este y si no la normal
            serializer = UserSignUpSerializer(data=request.data)
        else:
            serializer = UserSignUpNoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        """if user:
            User.objects.filter(id=user.id).update(groups=request.data['groups'])"""
        data = UserSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request' : self.request}


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request' : self.request}










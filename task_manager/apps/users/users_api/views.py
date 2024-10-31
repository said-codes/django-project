from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.serializers import TaskSerializer, UserSerializer, CustomerSerializer
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

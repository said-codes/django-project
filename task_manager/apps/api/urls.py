from django.urls import path,include
from rest_framework import routers
from apps.api import views
from apps.users import views as views_user



router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='User')
router.register(r'tasks',views.TaskViewSet)
router.register(r'users',views_user.UserViewSet)
router.register(r'customers',views.CustomerViewSet)
router.register(r'groups',views.GroupViewSet, basename='Group')
urlpatterns =[
    path('', include(router.urls)),
]


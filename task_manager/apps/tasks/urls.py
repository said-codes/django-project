from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/edit/<int:pk>/', views.task_edit, name='task_edit'),
    path('tasks/reactivate/<int:pk>/', views.task_reactivate, name='task_reactivate'),

]

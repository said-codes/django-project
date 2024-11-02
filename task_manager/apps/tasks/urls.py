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
    
    # Desde aca tareas pero con vresion de API
    path('tasks/list_api/', views.task_list_api, name='task_list_api'),
    path('tasks/edit_api/<int:pk>/', views.task_edit_api, name='task_edit_api'),
    path('tasks/detail_api/<int:pk>/', views.task_detail_api, name='task_detail_api'),
    path('tasks/delete_api/', views.task_delete_api, name='task_delete_api'),
    path('tasks/reactivate_api/', views.task_reactivate_api, name='task_reactivate_api'),







]

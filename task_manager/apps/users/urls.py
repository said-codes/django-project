from django.urls import path
from django.contrib.auth import views as auth_views
from apps.users import views
from .views import CustomLoginView
from .views import user_profile, CustomPasswordChangeView

urlpatterns = [
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html') , name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(next_page='next'), name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),  # Cambia 'next' a 'login'
    path('accounts/register/', views.register, name='register'),
    path('profile/', user_profile, name='profile'),
    path('change-password/', CustomPasswordChangeView.as_view(),
         name='change_password'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('users/reactivate/<int:user_id>/', views.user_reactivate, name='user_reactivate'),


    path('customers/', views.customer_list.as_view(), name='customer_list'),
    path('customers/create/', views.customer_create.as_view(),
         name='customer_create'),
    path('customers/edit/<int:pk>/',
         views.customer_update.as_view(), name='customer_edit'),
    path('customers/delete/<int:pk>/',
         views.customer_delete.as_view(), name='customer_delete'),


    #urls version api
    path('users/list_api/', views.user_list_api, name='user_list_api'),
    path('users/edit_api/<int:pk>/', views.user_edit_api, name='user_edit_api'),
    path('users/detail_api/<int:pk>/', views.user_detail_api, name='user_detail_api'),
    path('users/delete_api/', views.user_delete_api, name='user_delete_api'),
    path('users/reactivate_api/', views.user_reactivate_api, name='user_reactivate_api'),




]

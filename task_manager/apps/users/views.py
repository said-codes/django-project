from django.core.exceptions import ValidationError
import re
from .forms import UpdateProfilePictureForm, UpdateUserInfoForm
from django.contrib.auth import get_user_model
from .forms import RegisterForm  # Asegúrate de tener un formulario personalizado
from django.views import View
from .models import Customer
from .forms import CustomerForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .forms import EmailAuthenticationForm
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Funciones de Sesiones
def register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Encriptar la contraseña
            user.save()
            login(request, user)  # Iniciar sesión al usuario después del registro
            messages.success(request, '¡Te has registrado exitosamente!')
            return redirect('task_list')  # Redirige después de un registro exitoso
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegisterForm()  # Crea un nuevo formulario vacío para GET
    return render(request, 'accounts/register.html', {'form': form})




# Vista para listar todas las tareas
@login_required
def user_list(request):
    users = User.objects.all()  # Obtiene todos los usuarios
    user = request.user
    groups = user.groups.all()
    grupos = [grupo.name for grupo in groups]
    users = None
    if "Consultor" in grupos:
        users = User.objects.filter(enabled=True).order_by("-enabled")
    else:
        users = User.objects.all().order_by("-enabled")
    context = {
        'users': users,
        'title': 'Lista de Usuarios'
    }
    return render(request, 'users/user_list.html', context)


def user_create(request):
     groups = Group.objects.all()  # Obtener todos los grupos
     print(groups)  # Para verificar que los g
     if request.method == 'POST':
         form = UserForm(request.POST, request.FILES)
         if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password('defaultpassword')  # O permite que el usuario establezca su contraseña
            new_user.save()

            # Imprimir los grupos seleccionados para depuración
            print(form.cleaned_data['groups'])  # Asegúrate de que contenga los IDs correctos

            # Asignar grupos
            groups_ids = form.cleaned_data['groups']
            new_user.groups.set(groups_ids)  # Asigna los grupos seleccionados

            return redirect('user_list')
         else:
            print(form.errors)  # Para ver errores en el formulario
     else:
        form = UserForm()

     return render(request, 'users/user_create.html', {'form': form})


def user_edit(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')  # Mensaje de éxito
            return redirect('user_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'users/user_edit.html', {'form': form})



def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario o retorna 404 si no existe
    context = {
        'user': user,
        'title': 'Detalles del Usuario'
    }
    return render(request, 'users/user_detail.html', context)

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.enabled = False  # Cambia el estado a deshabilitado
    user.save()
    return redirect('user_list')  # Redirige a la lista de tareas

def user_reactivate(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.enabled = True  # Cambia el estado a habilitado
    user.save()
    return redirect('user_list')

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        # Puedes agregar lógica adicional aquí si es necesario
        return super().form_valid(form)


# Vista para ver el perfil del usuario
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        # Verificamos si el formulario que se envió es para la imagen o para la información personal
        if 'update_picture' in request.POST:
            picture_form = UpdateProfilePictureForm(request.POST, request.FILES, instance=user)
            info_form = UpdateUserInfoForm(instance=user)  # No procesamos info_form cuando se sube imagen
            if picture_form.is_valid():
                picture_form.save()
                messages.success(request, '¡Tu foto de perfil ha sido actualizada!')
                return redirect('profile')
        elif 'update_info' in request.POST:
            picture_form = UpdateProfilePictureForm(instance=user)  # No procesamos picture_form cuando se actualiza info
            info_form = UpdateUserInfoForm(request.POST, instance=user)
            if info_form.is_valid():
                info_form.save()
                messages.success(request, '¡Tu información personal ha sido actualizada!')
                return redirect('profile')
    else:
        picture_form = UpdateProfilePictureForm(instance=user)
        info_form = UpdateUserInfoForm(instance=user)

    context = {
        'picture_form': picture_form,
        'info_form': info_form,
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)


# Vista para cambiar la contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')  # Redirigir al perfil luego de cambiar la contraseña


# customers views

class customer_list(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customers/customer_list.html', {'customers': customers})

class customer_create(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'customers/customer_form.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
        return render(request, 'customers/customer_form.html', {'form': form})

class customer_update(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        return render(request, 'customers/customer_form.html', {'form': form})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
        return render(request, 'customers/customer_form.html', {'form': form})

class customer_delete(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return redirect('customer_list')



@login_required
def user_list_api(request):
   form = UserForm()
   user = request.user
   groups = user.groups.all()
   grupos = [grupo.name for grupo in groups]
   permisos = request.user.get_all_permissions()


   return render(request,'users/user_list_api.html',{'permisos': permisos,'form': form})

@login_required
def user_edit_api(request,pk):
    return render(request,'',{'pk':pk})


@login_required
def user_delete_api(request):
    return render(request,'',{})

@login_required
def user_reactivate_api(request):
    return render(request,'',{})

@login_required
def user_detail_api(request, pk):
    permisos = request.user.get_all_permissions()
    return render(request, 'users/user_detail_api.html',{'permisos':permisos, "pk":pk})

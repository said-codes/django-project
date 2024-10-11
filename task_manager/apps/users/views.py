from django.views import View
from .models import Customer
from .forms import CustomerForm  # Asegúrate de que tienes este formulario creado
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

# Funciones de Sesiones
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión al usuario después del registro
            messages.success(request, '¡Te has registrado exitosamente!')
            return redirect('task_list')  # Redirige a la lista de tareas
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})




# Vista para listar todas las tareas
@login_required
def user_list(request):
    users = User.objects.all()  # Obtiene todos los usuarios
    context = {
        'users': users,
        'title': 'Lista de Usuarios'
    }
    return render(request, 'users/user_list.html', context)

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)  # Asegúrate de que UserForm esté bien definido
        if form.is_valid():
            form.save()  # Guarda el formulario en la base de datos
            messages.success(request, 'Usuario creado exitosamente.')  # Mensaje de éxito
            return redirect('user_list')  # Asegúrate de que 'user_list' esté definido en tus urls
    else:
        form = UserForm()  # Si no es un POST, crea un nuevo formulario vacío

    context = {
        'form': form,
        'title': 'Crear Usuario'
    }
    return render(request, 'users/user_create.html', context)  # Renderiza la plantilla


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario o retorna 404 si no existe
    context = {
        'user': user,
        'title': 'Detalles del Usuario'
    }
    return render(request, 'users/user_detail.html', context)


def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Obtiene el usuario o retorna 404 si no existe
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)  # Pasamos la instancia del usuario
        if form.is_valid():
            form.save()  # Guarda los cambios en el usuario
            messages.success(request, 'Usuario actualizado exitosamente.')  # Mensaje de éxito
            return redirect('user_list')  # Redirige a la lista de usuarios
    else:
        form = UserForm(instance=user)  # Carga el formulario con los datos actuales del usuario

    context = {
        'form': form,
        'title': 'Editar Usuario'
    }
    return render(request, 'users/user_edit.html', context)


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('user_list')  # Redirige a la lista de usuarios

    context = {
        'user': user,
        'title': 'Eliminar Usuario'
    }
    return render(request, 'users/user_delete.html', context)

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        # Puedes agregar lógica adicional aquí si es necesario
        return super().form_valid(form)


# Vista para ver el perfil del usuario
def user_profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

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

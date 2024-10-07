from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone



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

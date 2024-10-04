from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_user(user):
    return user.groups.filter(name='Usuario').exists()

def is_consultant(user):
    return user.groups.filter(name='Consultor').exists()

def is_admin_or_user(user):
    return is_admin(user) or is_user(user)

def is_admin_or_user_or_consultant(user):
    return is_admin(user) or is_user(user) or is_consultant(user)

# Vista para listar todas las tareas
@login_required
def task_list(request):
    # Obtener los permisos del usuario actual
    permisos = request.user.get_all_permissions()
    print(permisos)
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, "permisos": permisos})

# Vista para crear una nueva tarea
@login_required
@user_passes_test(is_admin_or_user)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# Vista para editar una tarea existente
@login_required
@user_passes_test(is_admin_or_user)
def task_edit(request, pk):
    user = request.user
    group_permissions = user.get_group_permissions()
    if 'tasks.change_task' in group_permissions:
        task = get_object_or_404(Task, pk=pk)

        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('task_list')  # Redirige a la lista de tareas después de guardar.
        else:
            form = TaskForm(instance=task)

        return render(request, 'tasks/task_edit.html', {'form': form})
    else:
        return redirect('task_list')

# Vista para eliminar una tarea
@login_required
@user_passes_test(is_admin)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# Vista para ver los detalles de una tarea específica
@login_required
@user_passes_test(is_admin_or_user_or_consultant)
def task_detail(request, pk):
    permisos = request.user.get_all_permissions()
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task,'permisos':permisos})




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

    return render(request, 'tasks/register.html', {'form': form})




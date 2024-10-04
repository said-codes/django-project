from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# Vista para listar todas las tareas
@login_required
def task_list(request):
    user = request.user
    print("Este usario ingreso al listado de tareas", user)
    group_permissions = user.get_group_permissions()
    print("tiene estos permisos", group_permissions)
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks, "permisos": group_permissions})

# Vista para crear una nueva tarea
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
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

# Vista para ver los detalles de una tarea específica
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})




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




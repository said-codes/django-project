from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.api.serializers import TaskSerializer


# Vista para listar todas las tareas
@login_required
def task_list(request):
    # obtener el grupo al que pertenece
    user = request.user
    groups = user.groups.all()
    grupos = [grupo.name for grupo in groups]
    tasks = None
    if "consultor" in grupos:
        tasks = Task.objects.filter(enabled=True).order_by("-enabled")
    else:
        tasks = Task.objects.all().order_by("-enabled")

    # Obtener los permisos del usuario actual
    permisos = request.user.get_all_permissions()
    print(permisos)  # Solo obtiene tareas
    users = User.objects.all()
    for user in users:
        try:
            short_name = user.name_short()  # Aquí podría estar el error
            # Puedes hacer algo con short_name
        except IndexError as e:
            # Maneja el error aquí
            short_name = "Nombre no disponible"
            print(f"Error en name_short para el usuario {user.email}: {e}")

    for task in tasks:
        duration = task.duration  # Acceder como propiedad, sin paréntesis
        if duration:
            # Calcular días, horas y minutos
            task.duration_days = duration // (24 * 3600)  # Días
            task.duration_hours = (duration % (24 * 3600)) // 3600  # Horas
            task.duration_minutes = (duration % 3600) // 60  # Minutos
        else:
            task.duration_days = task.duration_hours = task.duration_minutes = None

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'users': users, "permisos": permisos})

@login_required
def task_list_api(request):
   tasks_api = None
   user = request.user
   groups = user.groups.all()
   grupos = [grupo.name for grupo in groups]
   permisos = request.user.get_all_permissions()


   return render(request,'tasks/task_list_api.html',{'permisos': permisos})

@login_required
def task_detail_api(request, pk):
    permisos = request.user.get_all_permissions()
    return render(request, 'tasks/task_detail_api.html',{'permisos':permisos, "pk":pk})

# Vista para crear una nueva tarea
@login_required
def task_create(request):
    user = request.user
    groups = user.groups.all()
    grupos = [grupo.name for grupo in groups]
    print("Grupos del usuario:", grupos)

    # Redirigir a la lista de tareas si el usuario es un consultor
    if "consultor" in grupos:
        return redirect("task_list")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # No guardes inmediatamente
            # Aquí no es necesario asignar created_at, ya que está manejado por el modelo
            task.save()  # Ahora guarda la tarea
            # Mensaje de éxito
            messages.success(request, "Tarea creada exitosamente.")
            return redirect('task_list')
        else:
            # Mensaje de error
            messages.error(
                request, "Error al crear la tarea. Por favor verifica los datos.")
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})


# Vista para editar una tarea existente
@login_required
def task_edit(request, pk):
    user = request.user
    print("Usuario username:", user.name)
    print("Usuario autenticado:", user.is_authenticated)

    if not user.is_authenticated:
        return redirect("login")

    groups = user.groups.all()
    grupos = [grupo.name for grupo in groups]
    print("Grupos del usuario:", grupos)

    if "consultor" in grupos:
        return redirect("task_list")

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # Redirige a la lista de tareas después de guardar.
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {'form': form})

@login_required
def task_edit_api(request,pk):
    return render(request,'',{'pk':pk})


@login_required
def task_delete_api(request):
    return render(request,'tasks/task_confirm_delete_api.html',{})

@login_required
def task_reactivate_api(request):
    return render(request,'tasks/task_confirm_reactivate_api.html',{})

# Vista para ver los detalles de una tarea específica
@login_required
def task_detail(request, pk):
    permisos = request.user.get_all_permissions()
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task, 'permisos': permisos})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.enabled = False  # Cambia el estado a deshabilitado
    task.save()
    return redirect('task_list')  # Redirige a la lista de tareas


def task_reactivate(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.enabled = True  # Cambia el estado a habilitado
    task.save()
    return redirect('task_list')



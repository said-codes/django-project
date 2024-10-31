class Task {
    constructor(createdAt, completedAt) {
        this.createdAt = new Date(createdAt)  // Fecha de creación
        this.completedAt = completedAt ? new Date(completedAt) : null  // Fecha de finalización
    }

    get duration() {
        if (this.completedAt) {
            const durationSeconds = Math.floor((this.completedAt - this.createdAt) / 1000)  // Calcula la duración en segundos
            return durationSeconds
        }
        return null
    }

    formattedDuration() {
        const duration = this.duration

        if (duration !== null) {
            const days = Math.floor(duration / (24 * 3600))
            const hours = Math.floor((duration % (24 * 3600)) / 3600)
            const minutes = Math.floor((duration % 3600) / 60)
            const seconds = duration % 60

            const durationParts = []
            if (days > 0) {
                durationParts.push(`${days} días`)
            }
            if (hours > 0) {
                durationParts.push(`${hours} horas`)
            }
            if (minutes > 0) {
                durationParts.push(`${minutes} minutos`)
            }
            if (seconds > 0) {
                durationParts.push(`${seconds} segundos`)
            }
            return durationParts.join(', ')
        }
        return "No disponible"
    }
}

async function loadTasks() {
    try {
        const response = await axios.get('/api/v1/tasks/') // Cambia la URL según tu configuración
        const tasks = response.data
        const tbody = document.querySelector('#tasksTable tbody')
        tbody.innerHTML = '' // Limpiar el contenido existente

        tasks.forEach(taskData => {
            const task = new Task(taskData.created_at, taskData.completed_at)
            console.log(task.formattedDuration())  // Salida: "2 días, 2 horas, 30 minutos"
            const row = document.createElement('tr')
            //console.log(taskData.change_task);

            row.innerHTML = `
                <td>
                    ${taskData.enabled ? `<a href="/tasks/detail/api/v1/?task_id=${taskData.id}/">${taskData.title}</a>` : `<span style="text-decoration: line-through;">${taskData.title}</span>`}
                </td>
                <td>${taskData.description}</td>
                <td>${new Date(taskData.created_at).toLocaleString()}</td>
                <td>${new Date(taskData.updated_at).toLocaleString()}</td>
                <td>
                    ${taskData.completed ? '<span class="badge bg-success">Completado</span>' : '<span class="badge bg-danger">No Completado</span>'}
                </td>
                <td>${task.formattedDuration()}</td>
            `

            if (taskData.enabled) {
                console.log(taskData.id)
                row.innerHTML += `
                    <td class="d-flex justify-content-around">
                        <a href="/tasks/edit/api/v1/?task_id=${taskData.id}/" class="btn btn-warning btn-circle btn-sm mx-1" title="Editar"><i class="fas fa-edit"></i></a>
                        <a href="/tasks/delete/api/v1/?task_id=${taskData.id}/" class="btn btn-danger btn-circle btn-sm mx-1" title="Eliminar"><i class="fas fa-trash"></i></a>
                        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#detailModal">
                        Detalle de Tarea
                        </button>
                        <a href="/tasks/detail/api/v1/?task_id=${taskData.id}/" class="btn btn-info btn-circle btn-sm mx-1" title="Detalles"><i class="fas fa-info-circle"></i></a>
                    </td>`
            } else {
                row.innerHTML += `
                    <td class="d-flex justify-content-around">
                        <a href="/tasks/edit/api/v1/?task_id=${taskData.id}/" class="btn btn-warning btn-circle btn-sm mx-1" title="Editar"><i class="fas fa-edit"></i></a>
                        <a href="/tasks/reactivate/api/v1/?task_id=${taskData.id}/" class="btn btn-success btn-circle btn-sm" title="Reactivar"><i class="fas fa-redo"></i></a>
                        <a href="/tasks/detail/api/v1/?task_id=${taskData.id}/" class="btn btn-info btn-circle btn-sm mx-1" title="Detalles"><i class="fas fa-info-circle"></i></a>
                    </td>`
            }

            tbody.appendChild(row)
        })
    } catch (error) {
        console.error('Error loading tasks:', error)
    }
}

// Cargar tareas al cargar la página
document.addEventListener('DOMContentLoaded', loadTasks)

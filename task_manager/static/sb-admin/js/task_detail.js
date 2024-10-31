  // Obtener el parámetro task_id de la URL
  const urlParams = new URLSearchParams(window.location.search);
  const taskId = urlParams.get('task_id'); // Esto obtiene el valor de task

  // script.js

// Función para obtener los detalles de la tarea
function getTaskDetails(taskId) {
    axios.get(`/api/v1/tasks/${taskId}/`) // Asegúrate de que esta URL sea la correcta
        .then(response => {
            const task = response.data;
            console.log(task)
            document.getElementById('task-title').innerText = task.title;
            document.getElementById('task-description').innerText = task.description;
            document.getElementById('task-created-at').innerText = new Date(task.created_at).toLocaleString();
            document.getElementById('task-updated-at').innerText = new Date(task.updated_at).toLocaleString();
            document.getElementById('task-completed').innerText = task.completed ? 'Sí' : 'No';

            // Si tienes permisos para editar y eliminar, añade la URL
            const editTaskLink = document.getElementById('edit-task');
            if (editTaskLink) {
                editTaskLink.href = `/tasks/edit/api/v1/?task_id=${taskId}`; // Ajusta la URL de edición según tu configuración de URL
            }

            const deleteTaskLink = document.getElementById('delete-task');
            if (deleteTaskLink) {
                deleteTaskLink.href = `/tasks/delete/?task_id=${taskId}`; // Ajusta la URL de eliminación según tu configuración de URL
            }
        })
        .catch(error => {
            console.error('Error al obtener los detalles de la tarea:', error);
            // Aquí puedes manejar el error, como mostrar un mensaje al usuario
        });
}

// Llamar a la función para obtener los detalles de la tarea
getTaskDetails(taskId);



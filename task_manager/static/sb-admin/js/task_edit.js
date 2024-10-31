document.addEventListener('DOMContentLoaded', async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('task_id');  // Asegúrate de que estás pasando el task_id en la URL

    if (taskId) {
        try {
            // Obtener los datos de la tarea desde la API
            const response = await axios.get(`/api/v1/tasks/${taskId}/`);
            const task = response.data;

            // Rellenar los campos del formulario con los datos de la API
            document.getElementById('title').value = task.title;
            document.getElementById('description').value = task.description;
            document.getElementById('completed').checked = task.completed;
        } catch (error) {
            console.error('Error al obtener la tarea:', error);
        }
    }

    // Enviar el formulario y actualizar la tarea
    document.getElementById('edit-task-form').addEventListener('submit', async function (e) {
        e.preventDefault();

        const updatedTask = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            completed: document.getElementById('completed').checked
        };

        try {
            await axios.put(`/api/v1/tasks/${taskId}`, updatedTask, {
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            window.location.href = taskListApiUrl;
        } catch (error) {
            console.error('Error al actualizar la tarea:', error);
        }
    });
});



document.addEventListener('DOMContentLoaded', async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const taskId = urlParams.get('task_id');  // Asegúrate de que estás pasando el task_id en la URL

    if (taskId) {
        try {
            // Obtener los datos de la tarea desde la API
            const response = await axios.get(`/api/v1/tasks/${taskId}/`);
            const task = response.data;

            // Enviar el formulario y actualizar la tarea
            document.getElementById('reactivate-task-form').addEventListener('submit', async function (e) {
                e.preventDefault();

               function toggle(){
                  if(task.enabled == true){
                    return task.enabled = false;
                  }else{
                    return task.enabled = true;
                  }
                }
                const updatedTask = {
                    title: task.title,
                    description: task.description,
                    completed: task.completed,
                    enabled: toggle()
                };

                try {
                    await axios.put(`/api/v1/tasks/${taskId}`, updatedTask, {
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    });

                    window.location.href = "http://localhost:8000/tasks/list/api/v1/";
                } catch (error) {
                    console.error('Error al actualizar la tarea:', error);
                }
            });
          } catch (error) {
            console.error('Error al obtener la tarea:', error);
          }
        }

      });




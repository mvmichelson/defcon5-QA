
// INDICE
// ======

// Mensajes en opciones
// Confirma Borrado de un Registro


// ==========================================================================================


// Mensajes en opciones
// ====================
// Aplicar con el CSS #comicBalloon 

// Inhibir actualizacion de Scroll

// Seleccion de Servicios




document.addEventListener('DOMContentLoaded', function() {
    const balloon = document.getElementById('comicBalloon');
    console.log('Entra a comicBalloon');
    //    console.log('Entra a comicBalloon', document.body.innerHTML);

    
    document.querySelectorAll('.link').forEach(link => {
        // Mostrar el globo de cómic con el mensaje específico cuando el cursor entra en el enlace
        link.addEventListener('mouseenter', function(event) {
            const message = link.getAttribute('data-message');
            balloon.textContent = message;
            balloon.style.display = 'block';
        });

        // Actualizar la posición del globo de cómic conforme se mueve el cursor
        link.addEventListener('mousemove', function(event) {
            const offsetX = -200;  // Ajuste para centrar horizontalmente
            const offsetY = -70;   // Ajuste para colocar debajo del cursor
            balloon.style.top = (event.pageY + offsetY) + 'px';
            balloon.style.left = (event.pageX + offsetX) + 'px';
        });

        // Ocultar el globo de cómic cuando el cursor sale del enlace
        link.addEventListener('mouseleave', function() {
            balloon.style.display = 'none';
        });
    });
});

// Confirma Borrado de un Registro
// ===============================
// Recibe el Mensaje como parametro
// Se usa con CSS #confirmation-dialog

document.addEventListener("DOMContentLoaded", () => {
    console.log('Entre a Confirmacion de Borrado:');

    const dialog = document.getElementById("confirmation-dialog");
    const messageElem = document.getElementById("confirmation-message");
    const confirmYes = document.getElementById("confirm-yes");
    const confirmNo = document.getElementById("confirm-no");

    let targetHref = null;

    // Manejar el clic en los enlaces con la clase 'confirm-link'
    document.querySelectorAll(".confirm-link").forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault(); // Prevenir la redirección inmediata
            targetHref = link.href; // Guardar la URL del enlace
            const message = link.getAttribute("con-message") || "¿Está seguro?";
            messageElem.textContent = message;
            dialog.classList.remove("hidden"); // Mostrar el cuadro de confirmación
        });
    });

    // Manejar el botón "Sí"
    confirmYes.addEventListener("click", () => {
        if (targetHref) {
            window.location.href = targetHref; // Redirigir al enlace
        }
        dialog.classList.add("hidden"); // Ocultar el cuadro de confirmación
    });

    // Manejar el botón "No"
    confirmNo.addEventListener("click", () => {
        targetHref = null; // Limpiar la URL guardada
        dialog.classList.add("hidden"); // Ocultar el cuadro de confirmación
    });
});


// Registrar Comentarios en Revision de Etapas del Proceso.
// =======================================================

document.addEventListener("DOMContentLoaded", function () {
    const commentBox = document.getElementById("comment-box");
    const commentText = document.getElementById("comment-text");
    let currentField = null;
    let currentId = null;
    let currentSec = null;

    console.log('Entra a Comentario de Revisión');

    // Abrir la caja de comentarios al hacer clic en el ícono X
    document.querySelectorAll(".comment-icon").forEach(icon => {
        icon.addEventListener("click", function () {
            console.log('Entra al hacer Click');

            currentField = icon.getAttribute("data-field");
            currentId = icon.getAttribute("data-id");
            currentSec = icon.getAttribute("data-sec");

            console.log('currentField =', currentField);
            console.log('currentId =', currentId);


            commentBox.classList.remove("hidden");
            commentText.value = "";
            commentText.focus();
        });
    });

    // Guardar el comentario al hacer clic en "Enviar Comentario"
    document.getElementById("save-comment").addEventListener("click", function () {
        const comment = commentText.value; // Obtener el comentario del textarea

        // Validar que el comentario no esté vacío
        if (!comment) {
            alert("Por favor, escribe un comentario antes de enviar.");
            return; // Salir si el comentario está vacío
        }

        // const url = "{% url 'Crea-Rev-OC' %}";

        //fetch('/CIS/Auditorias/revisa/', {
        fetch('/bcp/revisa/', {

            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")  // Incluye el token CSRF si es necesario
            },
            body: JSON.stringify({
                obj_id: currentId,     // ID de la instancia de Proceso
                field: currentField,   // El campo que se está comentando
                seccion:currentSec,    // Seccion del Formulario de Revision 
                comment: comment       // El comentario ingresado por el usuario
            })
        })
        .then(response => {
            if (!response.ok) {
                console.log('obj_id =', obj_id)

                console.log('Error status:', response.status); // Ej. 404
                console.log('Error message:', response.statusText); // Ej. "Not Found"
                console.log('URL utilizada:', response.url); // Muestra la URL de la solicitud
                throw new Error('Error en la solicitud: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert("Comentario guardado.");
            } else {
                alert("*** Error al guardar el comentario. ***");
            }
        })
        .catch(error => {
            console.error("Error al guardar el comentario:", error);
        })
        .finally(() => {
            // Limpiar el área de texto y cerrar la caja
            commentText.value = '';
            commentBox.classList.add("hidden");
        });
    });

    // Cerrar la caja de comentarios
    document.getElementById("close-comment").addEventListener("click", function () {
        commentBox.classList.add("hidden");
    });

    // Función para obtener el CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


// Inhibir actualizacion de Scroll

document.addEventListener('DOMContentLoaded', function() {
    var barraScroll = document.querySelector('.BarraScroll');
  
    // Restaurar la posición del scroll desde sessionStorage al cargar la página
    if (sessionStorage.getItem('scrollPosition')) {
        console.log('Restaura');
        barraScroll.scrollTop = sessionStorage.getItem('scrollPosition');
    }
  
    // Guardar la posición del scroll en sessionStorage cuando el usuario hace scroll
    barraScroll.addEventListener('scroll', function() {
        console.log('Guarda posicion mientras se hace scroll');
        sessionStorage.setItem('scrollPosition', barraScroll.scrollTop);
    });
  
    // Interceptar el evento de carga de contenido
    window.addEventListener('beforeunload', function() {
        // Guardar la posición del scroll antes de que la página se recargue
        console.log('Guarda la posición del scroll antes de que la página se recargue');
  
        sessionStorage.setItem('scrollPosition', barraScroll.scrollTop);
    });
  });


  


// Seleccion de Servicios
// ======================

// Aseguramos que el script se ejecute solo cuando el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    console.log("Entra a Seleccion Servicios ");

    // Verificamos si los elementos existen antes de agregarles event listeners
    let filtroDisponibles = document.getElementById("filtro_disponibles");
    let filtroAsignados = document.getElementById("filtro_asignados");

    if (filtroDisponibles) {
        filtroDisponibles.addEventListener("input", function() {
            filtrarTabla("filtro_disponibles", "tabla_disponibles");
        });
    } else {
        console.warn("⚠️ Elemento 'filtro_disponibles' no encontrado en el DOM.");
    }

    if (filtroAsignados) {
        filtroAsignados.addEventListener("input", function() {
            filtrarTabla("filtro_asignados", "tabla_asignados");
        });
    } else {
        console.warn("⚠️ Elemento 'filtro_asignados' no encontrado en el DOM.");
    }

    // Asegurar que el formulario actualiza el input oculto antes de enviarse
    let formulario = document.querySelector("form");
    if (formulario) {
        formulario.addEventListener("submit", function(event) {
            actualizarRecursosSeleccionados();
        });
    }
});

function moverRecurso(boton, tablaDestinoId) {
    let fila = boton.closest("tr");  // Encuentra la fila del botón
    let tablaOrigen = fila.closest("table");  // Encuentra la tabla de origen
    let tablaDestino;

    // Determinar a qué tabla mover la fila
    if (tablaDestinoId === "id_tabla_asignados") {
        tablaDestino = document.querySelector("#tabla_asignados tbody");
    } else if (tablaDestinoId === "id_tabla_disponibles") {
        tablaDestino = document.querySelector("#tabla_disponibles tbody");
    } else {
        console.error(`Error: La tabla destino con id '${tablaDestinoId}' no existe.`);
        return;
    }

    if (!tablaDestino) {
        console.error(`Error: No se encontró el tbody de la tabla destino con id '${tablaDestinoId}'.`);
        return;
    }

    // Mover la fila a la nueva tabla
    tablaDestino.appendChild(fila);

    // Cambiar el botón para mover en sentido contrario
    if (tablaDestinoId === "id_tabla_asignados") {
        boton.innerHTML = "◀";
        boton.setAttribute("onclick", "moverRecurso(this, 'id_tabla_disponibles')");
    } else {
        boton.innerHTML = "▶";
        boton.setAttribute("onclick", "moverRecurso(this, 'id_tabla_asignados')");
    }

    // Actualizar el campo oculto después de mover
    actualizarRecursosSeleccionados();
}

function actualizarRecursosSeleccionados() {
    let recursosInput = document.getElementById("recursos_input");
    let filas = document.querySelectorAll("#tabla_asignados tbody tr");

    let recursosSeleccionados = [];
    filas.forEach(fila => {
        let recursoId = fila.getAttribute("data-id");
        if (recursoId) {
            recursosSeleccionados.push(recursoId);
        }
    });

    console.log("Recursos seleccionados antes de enviar:", recursosSeleccionados);

    // Actualizar el campo oculto con los IDs de los recursos asignados
    recursosInput.value = recursosSeleccionados.join(",");
}

// Función para filtrar la tabla
function filtrarTabla(inputId, tablaId) {
    let filtro = document.getElementById(inputId);
    let tabla = document.getElementById(tablaId);
    if (!filtro || !tabla) {
        console.warn(`⚠️ No se encontró el elemento con id '${inputId}' o '${tablaId}'.`);
        return;
    }

    let filtroTexto = filtro.value.toLowerCase();
    let filas = tabla.querySelectorAll("tbody tr");

    filas.forEach(fila => {
        let textoFila = fila.innerText.toLowerCase();
        if (textoFila.includes(filtroTexto)) {
            fila.style.display = "";
        } else {
            fila.style.display = "none";
        }
    });
}

console.log("Script main.js ejecutado correctamente.");

// Activa/Desactiva PC
// ===================

document.addEventListener("DOMContentLoaded", function () {
    console.log("main.js en Activa/Desactiva cargado correctamente");

    // Cargar estados actuales de los switches al iniciar la página
    fetch("/bcp/procedimientos/toggle/")  
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data.forEach(proc => {
                let toggle = document.querySelector(`#toggle-activo-${proc.id}`);
                if (toggle) {
                    toggle.checked = proc.esta_activo;
                }
            });
        })
        .catch(error => console.error("Error al obtener estados:", error));

    // Agregar eventos a los switch
    document.querySelectorAll("input[id^='toggle-activo-']").forEach(function (toggle) {
        toggle.addEventListener("change", function () {
            let procedimientoId = this.dataset.id;
            let isChecked = this.checked;

            console.log("Intentando cambiar estado...");
            console.log(`Switch cambiado: ${procedimientoId}, Estado: ${isChecked}`);

            if (!procedimientoId) {
                console.error("Error: No se encontró el ID del procedimiento en el dataset.");
                return;
            }

            console.log(`Enviando petición a: /bcp/procedimientos/toggle/${procedimientoId}/`); 
            
            fetch(`/bcp/procedimientos/toggle/${procedimientoId}/`, {  
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ esta_activo: isChecked })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Respuesta recibida:", data);
                if (data.success) {  
                    console.log("Estado cambiado correctamente:", data.nuevo_estado);
                } else {
                    alert("Error al actualizar el estado.");
                    toggle.checked = !isChecked;
                }
            })
            .catch(error => {
                console.error("Error en la petición:", error);
                toggle.checked = !isChecked;
            });
        });
    });

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                let trimmed = cookie.trim();
                if (trimmed.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
});



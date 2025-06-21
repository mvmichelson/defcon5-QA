
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
    console.log("main.js cargado correctamente");

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
});

// Hacer la función moverRecurso accesible globalmente
function moverRecurso(boton, tablaDestinoId) {
    let fila = boton.closest("tr");
    let nuevaTabla = document.getElementById(tablaDestinoId);

    if (!fila) {
        console.warn("⚠️ Error al mover recurso: la fila no existe.");
        return;
    }

    if (!nuevaTabla) {
        console.warn(`⚠️ Error al mover recurso: la tabla destino con id '${tablaDestinoId}' no existe.`);
        return;
    }

    // Verificar si `tablaDestinoId` es un <tbody> o si debemos buscarlo dentro de la tabla
    let nuevoTbody = nuevaTabla.tagName === "TBODY" ? nuevaTabla : nuevaTabla.querySelector("tbody");

    // Si no existe un <tbody>, lo creamos para evitar errores
    if (!nuevoTbody) {
        console.warn(`⚠️ La tabla destino '${tablaDestinoId}' no tiene un <tbody>. Creando uno...`);
        nuevoTbody = document.createElement("tbody");
        nuevaTabla.appendChild(nuevoTbody);
    }

    // Cambiar el botón para que mueva en sentido contrario
    let nuevoBoton = fila.querySelector("button");
    if (nuevoBoton) {
        let nuevaTablaId = fila.closest("table")?.id; // Obtener el id correcto de la tabla origen
        if (!nuevaTablaId) {
            console.warn("⚠️ No se pudo determinar la tabla de origen.");
            return;
        }
        nuevoBoton.onclick = function() {
            moverRecurso(this, nuevaTablaId);
        };
    }

    // Mover la fila al nuevo <tbody>
    nuevoTbody.appendChild(fila);
}

// Asignar la función a `window` para asegurar su accesibilidad global
window.moverRecurso = moverRecurso;

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

// Confirmar que el script se cargó sin errores
console.log("Script main.js ejecutado correctamente.");


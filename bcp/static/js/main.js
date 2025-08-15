
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


// -----------------------------------------------------------------------------------------  


// Seleccion de Servicios
// ======================

/*
 main.js - Script unificado de asignación
 v1.1 - 2025-08-12
 ----------------------------------------
 - Soporte para múltiples bloques de asignación con atributo data-asignacion
 - Filtros para tablas disponibles y asignadas
 - Botones para mover filas entre tablas, con cambio de color y símbolo
 - Actualización automática de campo oculto (input hidden) antes de enviar el formulario
 - Logs detallados añadidos para debug
 ----------------------------------------
 Requisitos de HTML:
 - Contenedor principal con data-asignacion
 - Tablas con clases: .tabla-disponibles y .tabla-asignados
 - Inputs de filtro con clases: .filtro-disponibles y .filtro-asignados (opcionales)
 - Botones de mover con clase: .btn-mover y atributo data-destino ("asignados" o "disponibles")
 - Campo hidden con clase: .input-seleccion para enviar IDs seleccionados
*/

document.addEventListener("DOMContentLoaded", function () {
    console.log("📌 main.js v1.1 cargado correctamente");

    // Inicializar todos los bloques de asignación que existan en la página
    const bloques = document.querySelectorAll("[data-asignacion]");
    console.log(`🔹 Encontrados ${bloques.length} bloques de asignación`);
    bloques.forEach(function (bloque, index) {
        console.log(`➡️ Inicializando bloque #${index + 1}`);
        inicializarAsignacion(bloque);
    });
});

function inicializarAsignacion(contenedor) {
    let filtroDisponibles = contenedor.querySelector(".filtro-disponibles");
    let filtroAsignados = contenedor.querySelector(".filtro-asignados");
    let tablaDisponibles = contenedor.querySelector(".tabla-disponibles");
    let tablaAsignados = contenedor.querySelector(".tabla-asignados");

    console.log("  Inicializando filtros y botones en el bloque");

    if (filtroDisponibles) {
        filtroDisponibles.addEventListener("input", function () {
            console.log("  ▶ Filtrando tabla disponibles");
            filtrarTabla(filtroDisponibles, tablaDisponibles);
        });
    }
    if (filtroAsignados) {
        filtroAsignados.addEventListener("input", function () {
            console.log("  ▶ Filtrando tabla asignados");
            filtrarTabla(filtroAsignados, tablaAsignados);
        });
    }

    contenedor.querySelectorAll(".btn-mover").forEach(function (btn) {
        btn.addEventListener("click", function () {
            console.log(`  ▶ Botón mover clickeado, destino actual: ${btn.dataset.destino}`);
            moverFila(btn, contenedor);
        });
    });

    let formulario = contenedor.closest("form");
    if (formulario) {
        formulario.addEventListener("submit", function () {
            console.log("  ▶ Formulario enviado, actualizando selección");
            actualizarSeleccionados(contenedor);
        });
    }
}

function moverFila(boton, contenedor) {
    let fila = boton.closest("tr");
    let tablaDestino;

    if (boton.dataset.destino === "asignados") {
        tablaDestino = contenedor.querySelector(".tabla-asignados tbody");
        boton.dataset.destino = "disponibles";
        boton.textContent = "⏪";
        boton.style.background = "red";
        boton.style.color = "white";
        console.log(`    ↪ Moviendo fila ID ${fila.dataset.id} a asignados`);
    } else {
        tablaDestino = contenedor.querySelector(".tabla-disponibles tbody");
        boton.dataset.destino = "asignados";
        boton.textContent = "⏩";
        boton.style.background = "lightgreen";
        boton.style.color = "black";
        console.log(`    ↪ Moviendo fila ID ${fila.dataset.id} a disponibles`);
    }

    tablaDestino.appendChild(fila);
    actualizarSeleccionados(contenedor);
}

function actualizarSeleccionados(contenedor) {
    let inputHidden = contenedor.querySelector(".input-seleccion");
    let filas = contenedor.querySelectorAll(".tabla-asignados tbody tr");
    let ids = [];

    filas.forEach(f => {
        let id = f.dataset.id;
        if (id) ids.push(id);
    });

    inputHidden.value = ids.join(",");
    console.log(`  ✔ IDs seleccionados actualizados: [${inputHidden.value}]`);
}

function filtrarTabla(input, tabla) {
    let texto = input.value.toLowerCase();
    tabla.querySelectorAll("tbody tr").forEach(function (fila) {
        let visible = fila.innerText.toLowerCase().includes(texto);
        fila.style.display = visible ? "" : "none";
    });
    console.log(`  🔎 Filtrado aplicado con texto: "${input.value}"`);
}

// ======================================================================================


// Activa/Desactiva PC
// =====================================================================================

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
// ==========================================================================================



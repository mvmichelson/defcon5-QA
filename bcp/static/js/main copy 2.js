
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

            // 🚀 Forzar actualización de la página al finalizar el script
            setTimeout(() => {
                window.location.reload();
            }, 500);
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


// Inhibir actualizacion de Scroll (CSS BarraScroll)

document.addEventListener('DOMContentLoaded', function() {
    var barraScroll = document.querySelector('.BarraScroll');
    console.log('Activa Inhibidor de Barra de BarraScroll')
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
 main.js - Guardado inmediato al mover items (v1.0 comentada)
 - Al hacer click en botones .btn-mover, mueve la fila en el DOM y
   realiza un POST JSON al endpoint AJAX para persistir el cambio.
 - Si la petición falla, revierte la fila (rollback visual) y muestra toast.
 - Requiere en el HTML: el contenedor [data-asignacion] con atributos:
      data-model  = "app_label.ModelName"
      data-obj-id = "<id del objeto base>"
      data-field  = "<nombre_del_campo_M2M>"
 - Las filas <tr> deben tener data-id="{{ item.id }}"
*/

document.addEventListener("DOMContentLoaded", () => {
  console.log("main.js cargado: guardado inmediato al mover items");

  // Inicializa todos los bloques de asignación
  const bloques = document.querySelectorAll("[data-asignacion]");
  bloques.forEach(b => inicializarAsignacion(b));
});

function inicializarAsignacion(contenedor) {
  // registro de filtros si existen (no cambian funcionalidad previa)
  const filtroDisp = contenedor.querySelector(".filtro-disponibles");
  const filtroAsig = contenedor.querySelector(".filtro-asignados");
  if (filtroDisp) filtroDisp.addEventListener("input", () => filtrarTabla(filtroDisp, contenedor.querySelector(".tabla-disponibles")));
  if (filtroAsig) filtroAsig.addEventListener("input", () => filtrarTabla(filtroAsig, contenedor.querySelector(".tabla-asignados")));

  // asigna listeners a botones mover ya existentes
  contenedor.querySelectorAll(".btn-mover").forEach(btn => {
    btn.addEventListener("click", () => moverFilaYGuardar(btn, contenedor));
  });

  // si hay formulario, actualiza hidden al submit (compatibilidad)
  const form = contenedor.closest("form");
  if (form) form.addEventListener("submit", () => actualizarHidden(contenedor));
}

/*
 moverFilaYGuardar:
 - Mueve la fila visualmente al destino.
 - Actualiza el campo hidden que usaba el submit tradicional.
 - Realiza POST JSON al endpoint declarativo '/ajax/toggle_generic/' (o el que uses).
 - Si falla, revierte la fila al origen.
*/
function moverFilaYGuardar(boton, contenedor) {
  const fila = boton.closest("tr");
  if (!fila) return;

  // Determinar acción según data-destino actual del botón
  const destino = boton.dataset.destino; // "asignados" o "disponibles"
  let accion;
  let tablaDestino;

  if (destino === "asignados") {
    // el usuario está moviendo a "asignados" => acción añadir
    tablaDestino = contenedor.querySelector(".tabla-asignados tbody") || contenedor.querySelector(".tabla-asignados");
    accion = "add";
    // preparamos el botón para la próxima pulsación (ahora será 'disponibles')
    boton.dataset.destino = "disponibles";
    boton.textContent = "⏪";
    boton.style.background = "red";
    boton.style.color = "white";
  } else {
    tablaDestino = contenedor.querySelector(".tabla-disponibles tbody") || contenedor.querySelector(".tabla-disponibles");
    accion = "remove";
    boton.dataset.destino = "asignados";
    boton.textContent = "⏩";
    boton.style.background = "lightgreen";
    boton.style.color = "black";
  }

  // Guardar estado previo para posible rollback
  const padreOrigen = fila.parentElement;
  const siguientePrevio = fila.nextElementSibling; // para reinserción exacta

  // Mover visualmente
  tablaDestino.appendChild(fila);
  actualizarHidden(contenedor);

  // Preparar datos para el POST
  const model = contenedor.dataset.model;   // ej "bcp.Drp"
  const objId = contenedor.dataset.objId;   // ej 12
  const field = contenedor.dataset.field;   // ej "componentes"
  const itemId = fila.dataset.id;           // ej "34"

  // Si cualquiera de estos falta, no hacemos AJAX (compatibilidad retro)
  if (!(model && objId && field && itemId)) {
    console.log("AJAX no ejecutado: faltan data-* en el contenedor (compatibilidad local).");
    return;
  }

  // Endpoint donde está la vista Django. Ajusta si tu ruta es distinta.
  const url = "/bcp/ajax/toggle-generic/"; // asegúrate que coincide con urls.py


  // Construir payload JSON
  const payload = {
    model: model,
    obj_id: objId,
    field: field,
    item_id: itemId,
    action: accion
  };

  // CSRF: leer token del cookie o del input csrfmiddlewaretoken si lo prefieres
  const csrftoken = getCookie("csrftoken");

  // Control de timeout con AbortController para no colgar la UI
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify(payload),
    signal: controller.signal
  })
  .then(response => {
    clearTimeout(timeoutId);
    if (!response.ok) throw new Error("HTTP " + response.status);
    return response.json();
  })
  .then(data => {
    if (data.status === "ok") {
      // éxito: opcional mensaje pequeño
      toast(data.message || `Guardado: ${accion}`);
      console.log("AJAX OK:", data);
    } else {
      // backend respondió con error lógico (ej validación)
      throw new Error(data.message || "Error servidor");
    }
  })
  .catch(err => {
    console.error("Error guardando cambio via AJAX:", err);
    // Rollback visual: devolver fila al lugar original
    if (siguientePrevio && siguientePrevio.parentElement === padreOrigen) {
      padreOrigen.insertBefore(fila, siguientePrevio);
    } else {
      padreOrigen.appendChild(fila);
    }
    actualizarHidden(contenedor);
    toast("No se pudo guardar. Cambio revertido.", 2500);
  });
}

/* actualizarHidden: actualiza el input.hidden con la lista actual de ids asignados.
   Mantiene compatibilidad si alguien aún usa el envío del formulario.
*/
function actualizarHidden(contenedor) {
  const input = contenedor.querySelector(".input-seleccion");
  if (!input) return;
  const filas = contenedor.querySelectorAll(".tabla-asignados tbody tr, .tabla-asignados tr");
  const ids = Array.from(filas).map(r => r.dataset.id).filter(Boolean);
  input.value = ids.join(",");
}

/* util: obtener cookie por nombre (CSRF) */
function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(';') : [];
  for (let i = 0; i < cookies.length; i++) {
    const c = cookies[i].trim();
    if (c.startsWith(name + '=')) return decodeURIComponent(c.substring(name.length + 1));
  }
  return null;
}

/* util: pequeño toast para feedback */
function toast(msg, ms = 1400) {
  const el = document.createElement("div");
  el.textContent = msg;
  Object.assign(el.style, {
    position: "fixed", right: "18px", bottom: "18px",
    background: "rgba(0,0,0,0.8)", color: "white", padding: "8px 12px",
    borderRadius: "8px", zIndex: 99999, fontSize: "13px"
  });
  document.body.appendChild(el);
  setTimeout(() => el.remove(), ms);
}

/* filtrarTabla: igual que antes, con comentario para entender su ubicación */
function filtrarTabla(input, tabla) {
  if (!tabla) return;
  const term = input.value.toLowerCase();
  tabla.querySelectorAll("tbody tr, tr").forEach(row => {
    if (!row.dataset) return;
    row.style.display = row.innerText.toLowerCase().includes(term) ? "" : "none";
  });
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



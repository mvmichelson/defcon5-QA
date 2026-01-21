
// INDICE
// ======

// Mensajes en opciones
// Confirma Borrado de un Registro


// ==========================================================================================


// Mensajes en opciones
// ====================
// Aplicar con el CSS #comicBalloon 

// Inhibir actualización de Scroll (para todos los .BarraScroll y la ventana principal)

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



// Inhibir actualización de Scroll (para todos los .BarraScroll y la ventana principal)
// ====================================================================================

// Inhibidor de Scroll (para .BarraScroll y opcionalmente la ventana principal)
document.addEventListener('DOMContentLoaded', function() {
    console.log('Activa Inhibidor de Scroll');

    // 1️⃣ --- Para todos los contenedores con clase .BarraScroll ---
    const barras = document.querySelectorAll('.BarraScroll');
    barras.forEach((barra, i) => {
        const key = `scrollPositionInner_${i}`;
        const pos = sessionStorage.getItem(key);
        if (pos) barra.scrollTop = pos;

        barra.addEventListener('scroll', () => sessionStorage.setItem(key, barra.scrollTop));
        window.addEventListener('beforeunload', () => sessionStorage.setItem(key, barra.scrollTop));
    });

    // 2️⃣ --- Solo si el template tiene la marca meta ---
    const activarPrincipal = document.querySelector('meta[name="inhibir-scroll-principal"]');
    if (activarPrincipal) {
        console.log('Inhibidor principal ACTIVADO');

        const mainKey = 'scrollPositionMain';
        const posMain = sessionStorage.getItem(mainKey);
        if (posMain) window.scrollTo(0, posMain);

        window.addEventListener('scroll', () => {
            sessionStorage.setItem(mainKey, window.scrollY);
        });

        window.addEventListener('beforeunload', () => {
            sessionStorage.setItem(mainKey, window.scrollY);
        });
    } else {
        console.log('Inhibidor principal DESACTIVADO');
    }
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
            let incidenteId = this.dataset.incidente;   // 👈 NUEVO: lee el id del incidente

            console.log("Intentando cambiar estado...");
            console.log(`Switch cambiado: ${procedimientoId}, Estado: ${isChecked}`);
            console.log("incidente_id leído del dataset:", incidenteId); // 👈 NUEVO: muestra incidente_id en consola

            if (!procedimientoId) {
                console.error("Error: No se encontró el ID del procedimiento en el dataset.");
                return;
            }

            // 🚨 === CAMBIO AÑADIDO AQUÍ ===
            // Confirmación con SweetAlert2
            let mensajeConfirmacion = isChecked ? "Confirma Orden de Activación?" : "Confirma Orden de Desactivación?";
            Swal.fire({
                title: mensajeConfirmacion,
                text: "¿Deseas continuar con esta acción?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Sí, confirmar",
                cancelButtonText: "Cancelar",
                reverseButtons: true
            }).then((result) => {
                if (!result.isConfirmed) {
                    console.log("Cambio cancelado por el usuario.");
                    toggle.checked = !isChecked; // revierte el estado visual del switch
                    return;
                }

                console.log(`Enviando petición a: /bcp/procedimientos/toggle/${procedimientoId}/`); 
                
                fetch(`/bcp/procedimientos/toggle/${procedimientoId}/`, {  
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({ 
                        esta_activo: isChecked,
                        incidente_id: incidenteId    // 👈 NUEVO: envía el id del incidente al backend
                    })
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
                        Swal.fire({
                            icon: "success",
                            title: "Desactivacio exitosa",
                            text: isChecked ? "Se notificará via correo y wassap a gestores involucrados" : "Se notificará via correo y wassap a gestores involucrados",
                            timer: 8000,
                            showConfirmButton: false
                        });
                    } else {
                        Swal.fire("Error", "Error al actualizar el estado.", "error");
                        toggle.checked = !isChecked;
                    }
                })
                .catch(error => {
                    console.error("Error en la petición:", error);
                    Swal.fire("Error", "No se pudo conectar al servidor.", "error");
                    toggle.checked = !isChecked;
                });
            });
            // 🚨 === FIN DEL CAMBIO ===
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



// Activa/Desactiva cualquier booleano de cualquier Modelo
// =====================================================================================

document.addEventListener("DOMContentLoaded", function () {
    console.log("main.js en Activa/Desactiva GENERICO cargado correctamente");

    document.querySelectorAll(".toggle-switch").forEach(function (toggle) {
        toggle.addEventListener("change", function () {
            let app = this.dataset.app;
            let model = this.dataset.model;
            let id = this.dataset.id;
            let field = this.dataset.field;
            let value = this.checked;

            // === ✅ CAMBIO CLAVE ===
            // Usa mensajes personalizados si existen, o los genéricos si no.
            let mensajeConfirmacion = value
                ? (this.dataset.confirmOn || "Confirma Activación")
                : (this.dataset.confirmOff || "Confirma Desactivación");
            // === FIN CAMBIO ===

            Swal.fire({
                title: mensajeConfirmacion,
                text: "¿Deseas continuar con esta acción?",
                icon: "question",
                showCancelButton: true,
                confirmButtonText: "Sí, confirmar",
                cancelButtonText: "Cancelar",
                reverseButtons: true
            }).then((result) => {
                if (!result.isConfirmed) {
                    console.log("Cambio cancelado por el usuario.");
                    toggle.checked = !value;
                    return;
                }

                fetch(`/bcp/toggle/${app}/${model}/${id}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({ field: field, value: value })
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        Swal.fire("Error", "Error al actualizar el estado: " + data.error, "error");
                        toggle.checked = !value;
                    } else {
                        console.log(`Campo ${data.field} de ${data.model}(${data.id}) → ${data.nuevo_estado}`);
                        Swal.fire({
                            icon: "success",
                            title: "Actualización exitosa",
                            text: value ? "Activado correctamente." : "Desactivado correctamente.",
                            timer: 6000,
                            showConfirmButton: false
                        });
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    Swal.fire("Error", "No se pudo conectar al servidor.", "error");
                    toggle.checked = !value;
                });
            });
        });
    });

    // Obtiene token CSRF
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


// Enciende / Apaga LEDs  segun valor
// ===================================

// Este script:
// Lee data-value="{{ cantidad }}"
// Crea esa cantidad de LEDs
// Los enciende automáticamente 
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".led-panel").forEach(panel => {

    const value = Math.min(parseInt(panel.dataset.value) || 0, 10);

    let colorClass = "low";
    if (value >= 7) colorClass = "high";
    else if (value >= 4) colorClass = "medium";

    for (let i = 0; i < value; i++) {
      const led = document.createElement("span");
      led.className = `led ${colorClass}`;
      panel.appendChild(led);
    }

  });
});

// =====================================================================================


// ======================================================
// Detalle de Modelo (GENÉRICO) — VERSION COMPLETA
// ======================================================

// ⚠️ Obligatorio: función global (onclick la usa directamente)
window.abrirDetalleModelo = function(config) {

    console.log("1️⃣ entrar abrirDetalleModelo");
    console.log("2️⃣ config recibido =", config);
    console.log("3️⃣ URL_DETALLE_MODELO =", window.URL_DETALLE_MODELO);

    if (!window.URL_DETALLE_MODELO) {
        console.error("❌ URL_DETALLE_MODELO NO DEFINIDA");
        return;
    }

    fetch(window.URL_DETALLE_MODELO, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': obtenerCSRFToken()
        },
        body: JSON.stringify({
            modelo: config.modelo,
            id: config.id,
            listaCampos: config.listaCampos
        })
    })
    .then(response => {
        if (!response.ok) throw new Error("Respuesta HTTP inválida");
        return response.json();
    })
    .then(data => {
        const contenido = document.getElementById("detalle-contenido");
        contenido.innerHTML = ""; // Limpiar

        // === Título opcional ===
        if (config.titulo) {
                const tituloElem = document.createElement("div");
                tituloElem.className = "detalle-titulo";
                tituloElem.innerHTML = config.titulo; // ← AQUÍ
                contenido.appendChild(tituloElem);
            }


        // === Campos ===
        data.campos.forEach(item => {
            const div = document.createElement("div");

            if(item.lista){
                // Para ManyToMany
                div.textContent = `${item.label}: ${item.lista.join(", ")}`;
            } else {
                div.textContent = `${item.label}: ${item.valor}`;
            }

            contenido.appendChild(div);
        });

        // === Mensaje final opcional ===
        // if(config.mensajeFinal){
        //    const mensajeElem = document.createElement("p");
        //    mensajeElem.textContent = config.mensajeFinal;
        //    contenido.appendChild(mensajeElem);
        //}
        if (config.mensajeFinal) {
            const mensajeElem = document.createElement("div");
            mensajeElem.className = "detalle-mensaje";
            mensajeElem.innerHTML = config.mensajeFinal; // ← AQUÍ
            contenido.appendChild(mensajeElem);
        }


        // === Mostrar modal ===
        document.getElementById("modal-detalle-overlay").classList.remove("oculto");

    })
    .catch(err => {
        console.error("❌ Error en abrirDetalleModelo:", err);
        alert("No se pudo cargar el detalle del modelo");
    });
};

// ======================================================
// Cerrar modal
// ======================================================
window.cerrarDetalle = function() {
    const overlay = document.getElementById('modal-detalle-overlay');
    if(overlay){
        overlay.classList.add('oculto');
    }
};

// ======================================================
// Click fuera del modal
// ======================================================
document.addEventListener('click', function(e){
    const overlay = document.getElementById('modal-detalle-overlay');
    const modal = document.querySelector('.detalle-modal');

    if(!overlay || overlay.classList.contains('oculto')) return;
    if(modal && !modal.contains(e.target)){
        cerrarDetalle();
    }
});

// ======================================================
// CSRF helper
// ======================================================
function obtenerCSRFToken(){
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
}

// ======================================================
// FIN main.js
// ======================================================


// Semaforo de Riesgo
// ===========================================================================================
document.addEventListener("DOMContentLoaded", () => {
    console.log("main js: Semaforo de Riesgo");
    // Se seleccionan todos los semáforos en la página
    document.querySelectorAll(".semaforo").forEach(sem => {
        // Se extraen los datos del semáforo
        const ranking = parseFloat(sem.dataset.ranking);  // Convertir a número flotante
        const valorMax = parseFloat(sem.dataset.biaMax);  // Correcto: data-bia-max -> sem.dataset.biaMax
        const tramo1 = parseFloat(sem.dataset["tramo-1"]);
        const tramo2 = parseFloat(sem.dataset["tramo-2"]);

        // Si alguno de los valores es NaN, significa que no se ha definido correctamente
        if ([ranking, valorMax, tramo1, tramo2].some(v => isNaN(v))) {
            console.warn("Semáforo sin datos completos:", sem.dataset);
            // En este caso, no se hace nada más con ese semáforo
            return;
        }

        // Validamos que los valores tengan sentido
        if (valorMax <= 0) {
            console.warn(`El valor de valorMax debe ser mayor que 0, pero es ${valorMax}`);
            return;  // Si es incorrecto, no hacemos nada
        }

        if (tramo1 < 0 || tramo1 > 1 || tramo2 < 0 || tramo2 > 1) {
            console.warn(`Los tramos deben estar en el rango [0, 1]. Valores recibidos: tramo1=${tramo1}, tramo2=${tramo2}`);
            return;  // Si los tramos están fuera de rango, no hacemos nada
        }

        if (tramo1 > tramo2) {
            console.warn(`El tramo 1 debe ser menor o igual al tramo 2. Valores recibidos: tramo1=${tramo1}, tramo2=${tramo2}`);
            return;  // Si el tramo 1 es mayor que el tramo 2, no hacemos nada
        }

        // Calculamos el ratio: ranking dividido por valorMax
        const ratio = ranking / valorMax;

        // Limpiamos las luces antes de agregar la luz activa
        sem.querySelectorAll(".luz").forEach(l => l.classList.remove("on"));

        // Si ratio es 0, no encendemos ninguna luz
        if (ratio === 0) {
            return; // Salimos sin hacer nada si ratio es 0
        }

        // Según el valor de 'ratio', activamos la luz correspondiente
        if (ratio <= tramo1) {
            sem.querySelector(".verde").classList.add("on");
        } else if (ratio <= tramo2) {
            sem.querySelector(".amarillo").classList.add("on");
        } else {
            sem.querySelector(".rojo").classList.add("on");
        }
    });

});
console.log("ANTES de abrirDetalleModelo");


// ==========================================================================================



/* --- Lógica de Pagina Principal  DEFCON 5 --- */

document.addEventListener('DOMContentLoaded', function() {
    const logContainer = document.getElementById('live-logs-df5');
    
    if (logContainer) {
        const messages = [
            "Verificando integridad de nodos...",
            "Protocolo BCP activo y en espera.",
            "Sincronización con base de datos completa.",
            "Escaneo de amenazas externas: 0 detectadas.",
            "Estado del sistema: ÓPTIMO.",
            "Enlace con centro de crisis verificado."
        ];

        function addLogEntry() {
            const time = new Date().toLocaleTimeString();
            const randomMsg = messages[Math.floor(Math.random() * messages.length)];
            const entry = document.createElement('div');
            
            entry.style.marginBottom = "5px";
            entry.innerHTML = `<span style="color: #666;">[${time}]</span> > ${randomMsg}`;
            
            logContainer.prepend(entry);
            
            // Mantener solo los últimos 10 mensajes
            if (logContainer.childNodes.length > 10) {
                logContainer.removeChild(logContainer.lastChild);
            }
        }

        // Iniciar ciclo de logs cada 4 segundos
        setInterval(addLogEntry, 4000);
        addLogEntry(); // Primera entrada inmediata
    }
});


/* --- Animación de consola DEFCON 5 --- */
function initDefconLogs() {
    const container = document.getElementById('live-logs-container');
    if (!container) return;

    const msgs = [
        "Sincronizando nodos BCP...",
        "Integridad de bases de datos: OK",
        "Monitor de incidentes: Sin alertas",
        "Protocolo de comunicación en espera",
        "Estado del sistema: DEFCON 5"
    ];

    setInterval(() => {
        const p = document.createElement('div');
        const time = new Date().toLocaleTimeString();
        p.innerHTML = `<span style="color:#00ff41">[${time}]</span> > ${msgs[Math.floor(Math.random()*msgs.length)]}`;
        p.style.fontSize = "11px";
        container.prepend(p);
        if (container.childNodes.length > 6) container.lastChild.remove();
    }, 4000);
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initDefconLogs);


document.addEventListener('DOMContentLoaded', function() {
    const consoleElem = document.getElementById('dashboard-console');
    if (consoleElem) {
        const logEntries = [
            "SCANNING NETWORK NODES...",
            "BCP PROTOCOL: STANDBY",
            "DATA INTEGRITY: 100%",
            "NO INCIDENTS DETECTED",
            "SATELLITE LINK: STABLE"
        ];

        setInterval(() => {
            const entry = document.createElement('div');
            entry.innerHTML = `> ${logEntries[Math.floor(Math.random() * logEntries.length)]}`;
            entry.style.color = "#00ff41";
            entry.style.fontSize = "11px";
            consoleElem.prepend(entry);
            if (consoleElem.childNodes.length > 8) consoleElem.lastChild.remove();
        }, 3000);
    }
});

/* --- COMPLEMENTO: Consola de Dashboard DEFCON 5 --- */
function startDashboardConsole() {
    const consoleBox = document.getElementById('live-console-output');
    if (!consoleBox) return; // Solo se ejecuta si estamos en la página principal

    const techMessages = [
        "VERIFICANDO INTEGRIDAD DE NODOS...",
        "ENLACE SATELITAL: ESTABLE",
        "SISTEMA BCP: MODO VIGILANCIA",
        "SINCRONIZANDO DATOS RIA/BIA",
        "STATUS: DEFCON 5 (PAZ TOTAL)"
    ];

    setInterval(() => {
        const line = document.createElement('div');
        line.style.color = "#00ff41";
        line.style.fontSize = "11px";
        line.style.marginBottom = "4px";
        line.innerHTML = `> [${new Date().toLocaleTimeString()}] ${techMessages[Math.floor(Math.random()*techMessages.length)]}`;
        consoleBox.prepend(line);
        if (consoleBox.childNodes.length > 10) consoleBox.lastChild.remove();
    }, 3500);
}

// Escuchador para iniciar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', startDashboardConsole);

function startDashboardConsole() {
    const consoleBox = document.getElementById('live-console-output');
    if (!consoleBox) return;

    const techMessages = [
        "SINC NODOS BCP...",
        "ENLACE SAT: OK",
        "MODO VIGILANCIA",
        "SYNC RIA/BIA OK",
        "STATUS: DEFCON 5"
    ];

    setInterval(() => {
        const line = document.createElement('div');
        line.style.color = "#00ff41";
        line.innerHTML = `> ${techMessages[Math.floor(Math.random()*techMessages.length)]}`;
        consoleBox.prepend(line);
        if (consoleBox.childNodes.length > 6) consoleBox.lastChild.remove();
    }, 4000);
}
document.addEventListener('DOMContentLoaded', startDashboardConsole);


function startDashboardConsole() {
    const consoleBox = document.getElementById('live-console-output');
    if (!consoleBox) return;

    const messages = [
        "SINC NODOS BCP...",
        "ENLACE SATELITAL: OK",
        "SINCRONIZANDO RIA/BIA",
        "STATUS: DEFCON 5",
        "SIN ANOMALÍAS DETECTADAS"
    ];

    setInterval(() => {
        const line = document.createElement('div');
        line.innerHTML = `> ${messages[Math.floor(Math.random()*messages.length)]}`;
        consoleBox.prepend(line);
        if (consoleBox.childNodes.length > 8) consoleBox.lastChild.remove();
    }, 4000);
}

document.addEventListener('DOMContentLoaded', startDashboardConsole);

function startDashboardConsole() {
    const consoleBox = document.getElementById('live-console-output');
    if (!consoleBox) return;

    const messages = ["SYNC NODOS...", "ENLACE OK", "STATUS: D5", "BIA UPDATED", "NO ALERTS"];

    setInterval(() => {
        const line = document.createElement('div');
        line.innerHTML = `> ${messages[Math.floor(Math.random()*messages.length)]}`;
        consoleBox.prepend(line);
        if (consoleBox.childNodes.length > 5) consoleBox.lastChild.remove();
    }, 4000);
}
document.addEventListener('DOMContentLoaded', startDashboardConsole);

// main.js

/**
 * Prepara el documento para impresión y dispara el diálogo.
 * Intenta establecer el título de la página temporalmente para que el 
 * nombre del archivo PDF sea descriptivo.
 */
function generarPDF(codigo, nombre) {
    // Guardamos el título original
    const originalTitle = document.title;
    
    // Limpiamos caracteres extraños del nombre para el archivo
    const nombreLimpio = nombre.replace(/[/\\?%*:|"<>]/g, '-');
    
    // Cambiamos el título del documento (el navegador lo usa como nombre de archivo)
    document.title = `PC_${codigo}_${nombreLimpio}`;
    
    // Ejecutamos la impresión
    window.print();
    
    // Restauramos el título original después de un breve delay
    setTimeout(() => {
        document.title = originalTitle;
    }, 1000);
}

// main.js - Gestión de exportación a PDF
function generarPDF(codigo, nombre) {
    // Guardamos el título original de la pestaña
    const originalTitle = document.title;
    
    // Limpiamos el nombre de caracteres no permitidos en archivos
    const nombreLimpio = nombre.replace(/[/\\?%*:|"<>]/g, '-');
    
    // Cambiamos el título temporalmente (el navegador lo usa como nombre del PDF)
    document.title = `PC_${codigo}_${nombreLimpio}`;
    
    // Disparamos el diálogo de impresión
    window.print();
    
    // Restauramos el título original tras 1 segundo
    setTimeout(() => {
        document.title = originalTitle;
    }, 1000);
}
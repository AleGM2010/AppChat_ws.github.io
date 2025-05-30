
$( function(){

    console.log(user,room_id);
    // Esto es como se ve el url del cliente (para conectar al WebSocket)
    var url = 'ws://' + window.location.host + '/ws/room/' + room_id + '/';
    var chatSocket = new WebSocket(url);

    // el websocket hablamos que tenia 3 estados, onopen, onmessage y onclose
    chatSocket.onopen = function(e) {
        // Cuando se abre la conexión, se puede enviar un mensaje o realizar alguna acción
        console.log('Conexión abierta con el WebSocket');
    }
    chatSocket.onclose = function(e) {
        // Cuando se cierra la conexión, se puede manejar el cierre
        console.log('Conexión cerrada con el WebSocket');
    }

    // Se ejecuta cuando la página termina de cargarse
    window.onload = function() {
        // Agrega un evento 'click' al botón con id "btnMessage" (el botón "Enviar")
        // Cuando se haga clic, se llamará a la función sendMessage
        document.querySelector('#btnMessage').addEventListener('click', sendMessage);

        // Agrega un evento 'keypress' al campo de entrada con id "inputMessage"
        // Cuando se presione una tecla, se ejecutará la función que verifica si es Enter (keyCode 13)
        document.querySelector('#inputMessage').addEventListener('keypress', function(e) {
            // Verifica si la tecla presionada es Enter (keyCode 13)
            if (e.keyCode === 13) {
                // Si es Enter, llama a la función sendMessage para procesar el mensaje
                sendMessage();
            }
        });
    };

    // Función para enviar un mensaje
    function sendMessage() {
        // Selecciona el campo de entrada con id "inputMessage" y obtiene su valor
        var message = document.querySelector('#inputMessage');

        // Llama a la función loadMessageHTML con el valor del mensaje para mostrarlo en la interfaz
        
        // Verifica si el valor del mensaje, después de eliminar espacios, no está vacío
        if (message.value.trim() !== '') {
            // Si no está vacío, limpia el campo de entrada
            loadMessageHTML(message.value.trim());
            message.value = '';
        } else {
            console.log('El mensaje está vacío, no se enviará');
        }


    };

    // Función para cargar y mostrar el mensaje en el HTML
    function loadMessageHTML(m) {
        // Selecciona el elemento con id "boxMessages" (donde se muestran los mensajes)
        // y agrega un nuevo HTML con el mensaje recibido
        document.querySelector('#boxMessages').innerHTML += `
            <div class="alert alert-primary" role="alert">
                ${m}
                <div>
                    <small class="fst-italic fw-bold">${user}</small>
                    <small class="float-end">2023-12-27 08:33</small>
                </div>
            </div>
        `;
    };

})

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

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data)


        if (data.type === 'chat_message') {
            const msj = data.message
            const username = data.username
            const datetime = data.datetime
            
            document.querySelector('#boxMessages').innerHTML +=
            `
            <div class="alert alert-success" role="alert">
            ${msj}
            <div>
            <small class="fst-italic fw-bold">${username}</small>
            <small class="float-end">${datetime}</small>
            </div>
            </div>
            `
        }
        else if (data.type === 'user_list'){
            let userListHTML = ''
            let userClass = ''

            for( const username of data.users){
                if (username == user){
                    userClass = 'list-group-item-success'
                }
                userListHTML += `<li class="list-group-item ${userClass}">${username}</li>`
            }
            document.querySelector('#userList').innerHTML = userListHTML
        }

    }    

    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', function(e){
        if(e.keyCode == 13){
            sendMessage()
        }
    })

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
    function sendMessage(){
        var message = document.querySelector('#inputMessage')

        if(message.value.trim() !== ''){
            loadMessageHTML(message.value.trim())
            chatSocket.send(JSON.stringify({
                type: 'chat_message',
                message: message.value.trim(),
            }))

            console.log(message.value.trim())
            message.value = ''
        } else {
            console.log('Envió un mensaje vacío')
        }
    }

    // Función para cargar y mostrar el mensaje en el HTML
    function loadMessageHTML(m) {
        const dateObject = new Date();
        const year = dateObject.getFullYear();
        const month = String(dateObject.getMonth() + 1).padStart(2, '0'); // Meses empiezan desde 0
        const day = String(dateObject.getDate()).padStart(2, '0');
        const hours = String(dateObject.getHours()).padStart(2, '0');
        const minutes = String(dateObject.getMinutes()).padStart(2, '0');
        const seconds = String(dateObject.getSeconds()).padStart(2, '0');
        const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

        // Selecciona el elemento con id "boxMessages" (donde se muestran los mensajes)
        // y agrega un nuevo HTML con el mensaje recibido
        document.querySelector('#boxMessages').innerHTML +=
        `
        <div class="alert alert-primary" role="alert">
            ${m}
            <div>
                <small class="fst-italic fw-bold">${user}</small>
                <small class="float-end">${formattedDate}</small>
            </div>
        </div>
        `
    }

})

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# a las 3 funciones que tenemos en ChatConsumers asincroncas hay que incorporar
# La sincronizidad, eso se hace con async_to_sync

class ChatConsumer(WebsocketConsumer):
    """
    🗂️ Clase basada en CBV (Class-Based View) para WebSockets
    ——————
    • Lado del servidor: gestiona conexiones de clientes WebSocket.
    • Hereda de WebsocketConsumer, que provee métodos básicos:
       - connect(), receive(), disconnect(), send(), etc.
    """

    def connect(self):
        """
        🔌 Se activa cuando el cliente intenta abrir la conexión.
        • Cliente envía: websocket.connect
        • Servidor recibe: llama a connect()
        • Aquí deberías verificar/auth y luego:
            self.accept()  # Acepta la conexión
        """
        print('Conexión establecida')            # Log en servidor
        # Antes el print lo usabamos para saber si el metodo paso por acá , pero realmente
        # No habia una conexion establecida como tal

        # Ahora tenemos que generar un room_name o chanel , para que 
        # cada persona va a tener un ID especial, algo que determine que esa persona 
        # se conecte a esa sala en particular con un hash de seguridad
        self.id = self.scope['url_route']['kwargs']['room_id']
        print(self.id)

        self.accept()                             # Aceptamos el WebSocket

    def disconnect(self, close_code):
        """
        ❌ Se dispara cuando la conexión se cierra (cliente o servidor).
        • close_code: motivo de cierre (int)
        • Útil para limpiar recursos o notificar a otros usuarios.
        """
        print(f'Se ha desconectado (code={close_code})')
        # Aquí podrías quitar al usuario de la sala, actualizar estado, etc.

    def receive(self, text_data):
        try:

            """
            📨 Se ejecuta al recibir un mensaje de texto desde el cliente.
            • text_data: JSON en formato string enviado por cliente.
            """
            print('Mensaje recibido:', text_data)     # Log raw JSON

            # 1️⃣ Parseamos JSON a dict Python
            text_data_json = json.loads(text_data)
            #    Ejemplo recibido: {'message': '¡Hola sala!'}

            # 2️⃣ Extraemos datos concretos
            message = text_data_json['message']       # message: str

            # 3️⃣ Procesamiento extra (ej. validación, guardado en BD)
            #    En un MMORTS podrías interpretar comandos así:
            #    if message.startswith('/build'):
            #        coord = text_data_json['coord']  # {'x':10, 'y':5}
            #        crear_edificio(usuario, coord)

            # 4️⃣ Envío de respuesta al cliente (o broadcast a la sala)
            self.send(text_data=json.dumps({
                'message': message                    # reenviamos mismo mensaje
            }))
            #    Para un MMORTS, en lugar de eco podrías enviar:
            #    {
            #      'type': 'chat_message',
            #      'user': username,
            #      'text': message,
            #      'timestamp': '12:34'
            #    }

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar JSON: ', e)


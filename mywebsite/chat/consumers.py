import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Message

class ChatConsumer(WebsocketConsumer):
    # Definimos un diccionario de usuarios conectados - vacio en un inicio
    connected_users = {} # Proposito: cargar usuarios de un room cuando entran, sacarlos cuando salen
                         # Y enviar esa lista info a la js (para que se actualice 
                         # la lista de usuarios conectados)

    """
    🗂️ Clase basada en CBV para WebSockets
    Gestiona conexiones de clientes a salas de chat.
    """

    def connect(self):
        print('Conexión establecida')

        # Extraemos el ID de la sala desde la URL
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'sala_chat{self.id}'
        self.user = self.scope['user']  # Usuario conectado
        self.username = self.user.username if self.user.is_authenticated else None

        # Agregamos el usuario al dicc 
        if self.room_group_name not in self.connected_users:
            self.connected_users[self.room_group_name] = []
        if self.username:
            self.connected_users[self.room_group_name].append(self.username)
        # El codigo anterior lo que hace es que si el room_group_name no existe
        # en el diccionario, lo crea y añade el usuario conectado a la lista de usuarios

        print(f'Conectando a la sala: {self.room_group_name}')
        print(f'Canal del cliente: {self.channel_name}')
        print(f'Usuario conectado: {self.user}')

        # Añadir este canal al grupo correspondiente (sala)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        # Una vez aceptada la conexión, podemos enviar el diccionario de usuarios conectados
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            # Esto lo creamos anteriormente
            'type': 'user_list',
            'users': self.connected_users[self.room_group_name]
        })

    def disconnect(self, close_code):
        # Eliminamos el usuario del diccionario de usuarios conectados
        if self.username in self.connected_users[self.room_group_name]:
            self.connected_users[self.room_group_name].remove(self.username)

        # Actualizamos la lista de usuarios conectados en el grupo
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            # Esto lo creamos anteriormente
            'type': 'user_list',
            'users': self.connected_users[self.room_group_name]
        })
        print(f'Se ha desconectado (code={close_code})')

        # Quitamos el canal del grupo
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def user_list(self, event):
        #Enviar la lista de usuarios conectados a todos los clientes en la sala
        self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']  # Lista de usuarios conectados
        }))

    def receive(self, text_data):
        try:

            text_data_json = json.loads(text_data)
            event_type = text_data_json.get('type')
            if event_type == 'chat_message':
                message = text_data_json['message']
                # Identificamos al remitente si está autenticado
                if self.scope['user'].is_authenticated:
                    sender_id = self.scope['user'].id
                else:
                    sender_id = None

                if sender_id:
                    # Grabamos los datos en la BD
                    message_save = Message.objects.create(
                        user_id=sender_id, # Recordemos que Create lo valida y crea
                        room_id=self.id,
                        message=message)
                    message_save.save()  # Guardamos el mensaje en la base de datos
                    """ Recordemos que es un CHAT y no un FORO por lo que cuando se entra al chat
                        los mensajes no se cargan a la sala
                    """
                    # Sincronizamos
                    # Enviamos el mensaje a todos en la sala (menos a sí mismo)
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'username': self.user.username,
                            'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S'),
                            'sender_id': sender_id,
                        }
                    )
                else:
                    print("Usuario no autenticado, no se envía mensaje.")

            elif event_type == 'user_list':
                # Este evento lo manejamos de Javascript desde el lado del ciente
                pass

        except json.JSONDecodeError as e:
            print('Error al decodificar JSON:', e)
        except KeyError as e:
            print('Falta una clave en el JSON recibido:', e)
        except Exception as e:
            print('Error inesperado:', e)

    def chat_message(self, event):
        """
        Envia el mensaje a todos los usuarios del grupo excepto al emisor.
        """
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        current_user_id = self.user.id if self.user.is_authenticated else None

        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'username': username,
                'datetime': datetime,
            }))
        else:
            print('El mensaje no se reenvía a su emisor')



# a las 3 funciones que tenemos en ChatConsumers asincroncas hay que incorporar
# La sincronizidad, eso se hace con async_to_sync
# Creada a proposito con el numero 2 para repasar lo que se hizo sin tanto codigo

class ChatConsumer2(WebsocketConsumer):
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
        self.room_group_name = 'sala_chat%s' % self.id  # Nombre del grupo de sala
        # para el usuario es el
        self.user = self.scope['user']  # Usuario conectado (si está autenticado)

        print(f'Conectando a la sala: {self.room_group_name}')  # Log del grupo
        print(f'Conectando a la sala: {self.channel_name}')  

        print(self.id)
        # Tengo que conectar con estos parametros a este websocket
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        """ Teoria
            Paso a paso:
            self.channel_layer.group_add → es una corutina (async def)

            async_to_sync(...) → convierte esa corutina en una función normal

            El primer () ejecuta async_to_sync(...) y devuelve la función sincronizada.

            El segundo () ejecuta esa función sincronizada con argumentos.

        """
        self.accept()                             # Aceptamos el WebSocket

    def disconnect(self, close_code):
        """
        ❌ Se dispara cuando la conexión se cierra (cliente o servidor).
        • close_code: motivo de cierre (int)
        • Útil para limpiar recursos o notificar a otros usuarios.
        """
        print(f'Se ha desconectado (code={close_code})')
        # Aquí podrías quitar al usuario de la sala, actualizar estado, etc.
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)



    def receive(self, text_data):
        try:

            """
            📨 Se ejecuta al recibir un mensaje de texto desde el cliente.
            • text_data: JSON en formato string enviado por cliente.
            """

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

            # Obtenemos el ID del usuario conectado que envió el mensaje
            if self.scope['user'].is_authenticated:
                sender_id = self.scope['user'].id
            else:
                None

            if sender_id:
                async_to_sync(self.channel_layer.group_send)(self.room_group_name,  
                    {
                        'type': 'chat_message',  # Tipo de mensaje a enviar
                        'message': message,      # Mensaje recibido
                        'username': self.user.username,       # ID del usuario que envió el mensaje
                        'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S'),
                        'sender_id':sender_id    # Timestamp simulado (puedes usar datetime)
                    }
                )
            else:
                None

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar JSON: ', e)
        except KeyError as e:
            print('Falta una clave en el JSON recibido: ', e)
        except Exception as e:
            print('Error inesperado al procesar el mensaje:', e)


    def chat_message(self, event):
        """
        📡 Método para enviar mensajes a todos los clientes conectados.
        • Se llama desde group_send() con 'type': 'chat_message'.
        • event: dict con datos del mensaje.
        """
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        current_user_id = self.scope['user'].id
        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'message':message,
                'username': username,
                'datetime': datetime
            }))

    
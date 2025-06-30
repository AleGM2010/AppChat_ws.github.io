import json
import uuid
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import random
from .models import Player  # Importar el modelo Player
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

COLORS = [
    "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff",
     "#b25757", "#4bc54b", "#4b4bb0", "#c6c645", "#43aaaa", "#871487",
      "#6c1e1e", "#346234", "#2a2a40", "#4b4b0a", "#174c4c", "#614661",
]

def random_color():
    cl = random.choice(COLORS)
    print("El color es: "+cl)
    # Elegirlo y guardarlo en una base de datos con un
    return cl

# Diccionario para almacenar los colores asignados a cada jugador
player_colors = {}

class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = "sala"
            self.room_group_name = f"game_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            self.player_id = str(uuid.uuid4())

            # Consultar o crear el jugador en la base de datos de forma asíncrona
            player, created = await sync_to_async(Player.objects.get_or_create)(player_id=self.player_id)
            if created:
                # Si es un nuevo jugador, asignar un color aleatorio
                player.color = random_color()
                await sync_to_async(player.save)()  # Guardar el jugador de forma asíncrona

            self.color = player.color

            # Enviar mensaje de inicialización al cliente local
            await self.send_json({
                "type": "init",
                "playerId": self.player_id,
                "position": {"x": 0, "y": 0, "z": 0},
                "color": self.color
            })

            # Notificar a todos los demás clientes sobre el nuevo jugador
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "player_joined",
                    "playerId": self.player_id,
                    "position": {"x": 0, "y": 0, "z": 0},
                    "color": self.color
                }
            )

        except Exception as e:
            print("❌ Error en connect():", e)
            await self.close()


    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        # Eliminar al jugador de la base de datos al desconectarse
        await sync_to_async(Player.objects.filter(player_id=self.player_id).delete)()


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            command_type = data.get('type')

            if (command_type == 'kick_all'):
                # Llamar al método para kickear a todos los jugadores
                await self.kick_all_players()
                print(" Todos los jugadores han sido desconectados.")
                return
            

            player_id = data.get('playerId')
            position = data.get('position')

            if not player_id or not isinstance(position, dict):
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Datos mal formados'
                }))
                return

            # Enviar a todos la posición
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'broadcast_position',
                'playerId': player_id,
                'position': position
            })

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'JSON inválido'
            }))


    async def broadcast_position(self, event):
        try:
            # Intentar obtener el jugador desde la base de datos
            player = await sync_to_async(Player.objects.get)(player_id=event['playerId'])
            player_color = player.color
            
        except ObjectDoesNotExist:
            # Si el jugador no existe, manejar el error
            return  # Ignorar este mensaje

        # Enviar a todos (Unity deberá ignorar su propio ID)
        await self.send(text_data=json.dumps({
            'type': 'update',
            'playerId': event['playerId'],
            'position': event['position'],
            'color': player_color  # Incluir el color del jugador
        }))



    async def player_left(self, event):
        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'playerId': event['playerId']
        }))

    async def kick_all_players(self):
        print("🔴 Desconectando a todos los jugadores...")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'kick_player',
                'message': 'Has sido desconectado por el administrador.'
            }
        )
        # Limpiar la base de datos
        await sync_to_async(Player.objects.all().delete)()

    async def kick_player(self, event):
        # Enviar un mensaje de desconexión a cada cliente
        await self.send(text_data=json.dumps({
            'type': 'kick',
            'message': event['message']
        }))

        # Eliminar al jugador de la base de datos
        await sync_to_async(Player.objects.filter(player_id=self.player_id).delete)()

        # Notificar a los demás jugadores que este jugador ha salido
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_left',
                'playerId': self.player_id
            }
        )

        await self.close()

    async def player_joined(self, event):
        # Enviar información del nuevo jugador a todos los clientes
        await self.send(text_data=json.dumps({
            "type": "player_joined",
            "playerId": event["playerId"],
            "position": event["position"],
            "color": event["color"]
        }))
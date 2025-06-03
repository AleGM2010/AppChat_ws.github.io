import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
# Quiero traer un middelware de autenticacion 
# ¿Para que hago esto?, ¿cual es el proposito de este middleware y que es un middleware?
from channels.auth import AuthMiddlewareStack  # ✅ Este middleware envuelve las conexiones WebSocket con información de usuario autenticado.
# ¿Para qué hago esto?
# → Para que puedas acceder a `scope["user"]` en tus Consumers.
# ¿Qué es un middleware?
# → Es una capa intermedia que modifica o añade lógica antes de que la petición 
#   llegue al handler (ej. agregar el usuario a la conexión WebSocket).

# scope = información de contexto de la conexión.
# handler = lo que responde a un evento de conexión o mensaje.


#region Teoria
"""
Teoria: 

🧠 ¿Qué es un scope en Django Channels?
Es un diccionario que contiene información sobre la conexión actual (como contexto).

📦 Incluye:

scope["user"]: el usuario autenticado (si usás AuthMiddlewareStack)

scope["path"]: la URL de conexión

scope["type"]: tipo de conexión ("websocket", "http")

scope["session"]: la sesión actual

scope["headers"]: cabeceras HTTP

🧩 Es como request en vistas tradicionales, pero adaptado a conexiones WebSocket o ASGI.


🧠 ¿Qué es un handler?
Un handler es una función o método que recibe y responde a un evento.

Ejemplos en Django Channels:

connect() → handler que maneja cuando el cliente se conecta.

receive() → cuando el cliente envía un mensaje.

disconnect() → cuando se desconecta.

📌 Equivale a def get() o def post() en una vista CBV.


"""
#endregion

# Tambien el routing 
import chat.routing
import juego.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns + juego.routing.websocket_urlpatterns)
    ),
})


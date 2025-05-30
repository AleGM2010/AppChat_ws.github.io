import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
# Quiero traer un middelware de autenticacion 
# ¿Para que hago esto?, ¿cual es el proposito de este middleware y que es un middleware?
from channels.auth import AuthMiddlewareStack
# Tambien el routing 
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
})


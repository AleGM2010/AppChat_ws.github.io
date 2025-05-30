"""
Esto es 'equivalente' al urls.py PERO usando CONSUMERS en lugar de VIEWS.
"""

from django.urls import path
from .consumers import ChatConsumer

# En lugar de urlpatterns, usamos websocket_urlpatterns (es propio de Channels)
websocket_urlpatterns = [
    # ..'ws/chat/' es la ruta WebSocket que el cliente usará para conectarse
    # Tengo entendido que es 'invisible' al usuario. El usuario ve una url pero NO 
    # accede a ../ws/chat/ ¿Esto es asi? ¿Por que?
    path('ws/room/<room_id>', ChatConsumer.as_asgi()),
    # Fijate tambien que se usa 'as_asgi()' en lugar de 'as_view()'  !!

    # Django ni se entera solo con routing y consumers de que esto existe, entonces
    # se carga en asgi.py 
]
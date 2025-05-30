"""
Esto es 'equivalente' al urls.py PERO usando CONSUMERS en lugar de VIEWS.
"""

from django.urls import path
from .consumers import ChatConsumer

# En lugar de urlpatterns, usamos websocket_urlpatterns (es propio de Channels)
websocket_urlpatterns = [
    # ..'ws/chat/' es la ruta WebSocket que el cliente usará para conectarse

    path('ws/room/<room_id>', ChatConsumer.as_asgi()),
    # Fijate tambien que se usa 'as_asgi()' en lugar de 'as_view()'  !!

    # ¿El usuario ve esta URL? No exactamente.
    # → Esta ruta NO es accedida por el navegador como si fuera una vista.
    # → Es utilizada internamente por `new WebSocket("ws://...")` desde JS del cliente.
    # → No aparece en la barra de navegación ni es renderizada en HTML.

    # Django no conoce estas rutas por sí mismo (no usa urls.py aquí).
    # Por eso se deben incluir explícitamente en `asgi.py` mediante una ruta WebSocket.

]
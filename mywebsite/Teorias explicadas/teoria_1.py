# Video numero 2 => DE LA TEORIA A LA ACCION !!

# min 5:41

# Le puse .py para que copilot autocomplete y me sea mas facil, luego se lo quito

WSGI_APPLICATION = 'teoria.wsgi.application'
# qque carajo es WSGI? , es un estandar de python para aplicaciones web, que permite que el servidor web se comunique con la aplicacion web, y viceversa
# fue creado en 2003. usa una arquitectura de peticion-respuesta (sincrona)
# llamada Web Server Gateway Interface (WSGI)

# para esta aplicacion necesitamos ASGI
# llamada Asynchronous Server Gateway Interface (ASGI)
# existe un archivo llamado asgi.py que es el equivalente al wsgi.py
# es un protocolo compatible ocn FAST API y Django.
# PROTOCOLO de comunicacion asincronico 

# Asincrono significa que puede manejar muchas peticiones al mismo tiempo, 
# sin esperar a que una termine para empezar otra
# Procesamiento simultaneo de multiples solicitudes en un solo hilo, es la 
#evolucion de WSGI, ideal para apps de alto rendimiento y en tiempo real

# Imagenes super interesantes que explican la diferencia entre WSGI y ASGI
# La eficiencia diferencial es brutal 

# Volviendo a la imagen descriptiva de Django-Daphne-Redis, Yo necesito que la 
# parte asincrona tenga un servidor dedicado, para poder manejar la comunicación
# Para eso usamos la extencion 'Channels', ese servidor se lo da 'Channels-redis'
# Para instalar Channels-redis necesitamos el adicional 'Daphne'

# => Chanel, utiliza el 'Channel Layer' para manejar la comunicacion asincrona
# para que las instancias de la aplicacion puedan comunicarse entre si


# Instalamos y configuramos todo:
"""
pip install channels
pip install daphne
pip install channels-redis

"""

# De ejecutar runserver ahora veremos que NO Levanta ASGI , sino WSGI (por defecto)
"""
Agregamos al inicio de apps en settings.py

'daphne',
    ...

y 

ASGI_APPLICATION = 'mywebsite.asgi.application'

ademas en asgi.py agregamos:

from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})

y comentamos el 'application' que viene por defecto en asgi.py


"""

# A este punto al hacer runserver, veremos que levanta el servidor ASGI
# >>>> Starting ASGI/Daphne version 4.2.0 development server


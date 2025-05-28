# Video numero 4 => PUESTA A PUNTO ZONA CHAT

# Vamos a utilizar javascript para hacer la interaccion de los mensajes en la room (sala)

# Yo creo que esto mejor pedirselo a GPT o Grok.

# Entonces importaremos desde html los scripts de javascript que vamos a utilizar.

"""
Creamos el archivo chat.js en una carpeta static/js/ y lo enlazamos en el HTML.
Ademas de configurarlo en el settings.py de Django para que se sirva correctamente.

se va a 'STATIC_URL' y debajo se agrega

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

ademas de agregar la carpeta 'static' en STATICFILES_DIRS:
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

luego en urls.py del proyecto se agrega la configuracion para servir archivos estaticos en modo DEBUG:

siendo estas:

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""

# Lo correcta seria poder levantar el sv sin problemas y ver en la 'consola' de la pagina
# (F12) Si aparece el mensaje que pusimos en el chat.js


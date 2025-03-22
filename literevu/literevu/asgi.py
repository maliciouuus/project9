"""
Configuration ASGI pour le projet literevu.

Il expose le module ASGI comme une variable de niveau supérieur nommée ``application``.

Pour plus d'informations sur ce fichier, voir
https://docs.djangoproject.com/fr/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "literevu.settings")

application = get_asgi_application()

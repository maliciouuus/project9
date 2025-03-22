"""
Configuration WSGI pour le projet literevu.

Il expose le module WSGI comme une variable de niveau supérieur nommée ``application``.

Pour plus d'informations sur ce fichier, voir
https://docs.djangoproject.com/fr/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "literevu.settings")

application = get_wsgi_application()

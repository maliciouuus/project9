"""
Configuration des URLs pour le projet literevu.

Ce fichier définit les points d'entrée principaux de l'application :
- L'interface d'administration (/admin/)
- Les URLs de l'application principale (/)
- La gestion des fichiers média

Pour plus d'informations sur la configuration des URLs :
https://docs.djangoproject.com/fr/5.0/topics/http/urls/

Exemples de configurations :
1. Vues basées sur des fonctions :
    from mon_app import views
    path('', views.accueil, name='accueil')

2. Vues basées sur des classes :
    from mon_app.views import Accueil
    path('', Accueil.as_view(), name='accueil')

3. Inclusion d'autres configurations d'URLs :
    from django.urls import include
    path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Configuration des URLs principales
urlpatterns = [
    # Interface d'administration Django
    path("admin/", admin.site.urls),
    # URLs de l'application listings (racine du site)
    path("", include("listings.urls")),
]

# En développement : ajout de la gestion des fichiers média
# Cette configuration ne doit pas être utilisée en production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

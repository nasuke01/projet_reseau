from django.contrib import admin
from .models import Employe, Client, Document

# Ajout des modèles dans l'interface admin
admin.site.register(Employe)
admin.site.register(Client)
admin.site.register(Document)

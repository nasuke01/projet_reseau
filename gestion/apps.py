from django.apps import AppConfig


class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'
def ready(self):
        from .models import creer_roles
        creer_roles()
        import gestion.signals
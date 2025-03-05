from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver

# 🔹 Appliquer automatiquement les permissions lorsqu'un utilisateur est créé
@receiver(post_save, sender=User)
def assigner_permissions_utilisateur(sender, instance, created, **kwargs):
    if created:  # Si l'utilisateur est nouvellement créé
        if instance.groups.exists():  # Vérifie s'il appartient à un groupe
            permissions = Permission.objects.filter(group__in=instance.groups.all())  # Récupère ses permissions
            instance.user_permissions.set(permissions)  # Applique les permissions
            instance.save()

# 🔹 Mettre à jour les permissions quand un utilisateur rejoint ou quitte un groupe
@receiver(m2m_changed, sender=User.groups.through)
def appliquer_permissions_automatiques(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:  # Quand un utilisateur rejoint ou quitte un groupe
        if instance.groups.exists():
            permissions = Permission.objects.filter(group__in=instance.groups.all())  # Récupère les permissions du groupe
            instance.user_permissions.set(permissions)  # Applique les permissions du groupe
        else:
            instance.user_permissions.clear()  # Supprime les permissions si l'utilisateur n'a plus de groupe
        instance.save()

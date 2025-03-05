from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


# Modèle pour les employés
class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    poste = models.CharField(max_length=100)
    date_embauche = models.DateField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Modèle pour les clients
class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Modèle pour les documents
class Document(models.Model):
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents/')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


def creer_roles():
    groupes = {
        "Admin": ["add_employe", "change_employe", "delete_employe", 
                  "add_client", "change_client", "delete_client", 
                  "add_document", "delete_document"],
        "Employe": ["add_client", "change_client"],
        "Utilisateur": []
    }

    for role, permissions in groupes.items():
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f"Groupe '{role}' créé.")

        # Ajouter les permissions
        for perm_codename in permissions:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"⚠️ Permission {perm_codename} introuvable !")
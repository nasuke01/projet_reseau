from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.conf import settings
from .models import Employe, Client, Document
from .forms import EmployeForm, ClientForm, DocumentForm
import os


# ==========================
# 🔹 Vues pour les Employés
# ==========================

@login_required
@permission_required('gestion.view_employe', raise_exception=True)
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'gestion/liste_employes.html', {'employes': employes})


@login_required
@permission_required('gestion.add_employe', raise_exception=True)
def ajouter_employe(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'employé a été ajouté avec succès !")
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    return render(request, 'gestion/ajouter_employe.html', {'form': form})


@login_required
@permission_required('gestion.change_employe', raise_exception=True)
def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == "POST":
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, "L'employé a été modifié avec succès !")
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'gestion/modifier_employe.html', {'form': form})


@login_required
@permission_required('gestion.delete_employe', raise_exception=True)
def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    employe.delete()
    messages.success(request, "L'employé a été supprimé avec succès.")
    return redirect('liste_employes')


# ==========================
# 🔹 Vues pour les Clients
# ==========================

@login_required
@permission_required('gestion.view_client', raise_exception=True)
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'gestion/liste_clients.html', {'clients': clients})


@login_required
@permission_required('gestion.add_client', raise_exception=True)
def ajouter_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client a été ajouté avec succès !")
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'gestion/ajouter_client.html', {'form': form})


@login_required
@permission_required('gestion.change_client', raise_exception=True)
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client a été modifié avec succès !")
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'gestion/modifier_client.html', {'form': form})


@login_required
@permission_required('gestion.delete_client', raise_exception=True)
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    messages.success(request, "Le client a été supprimé avec succès.")
    return redirect('liste_clients')


# ==========================
# 🔹 Vues pour les Documents
# ==========================

@login_required
@permission_required('gestion.view_document', raise_exception=True)
def liste_documents(request):
    documents = Document.objects.all()
    return render(request, 'gestion/liste_documents.html', {'documents': documents})


@login_required
@permission_required('gestion.add_document', raise_exception=True)
def ajouter_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le document a été ajouté avec succès !")
            return redirect('liste_documents')
    else:
        form = DocumentForm()
    return render(request, 'gestion/ajouter_document.html', {'form': form})


@login_required
@permission_required('gestion.delete_document', raise_exception=True)
def supprimer_document(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()
    messages.success(request, "Le document a été supprimé avec succès.")
    return redirect('liste_documents')


# 🔹 Téléchargement sécurisé des fichiers
@login_required
@permission_required('gestion.view_document', raise_exception=True)
def telecharger_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    file_path = os.path.join(settings.MEDIA_ROOT, document.fichier.name)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


# ==========================
# 🔹 Authentification avec Redirection Dynamique
# ==========================

def connexion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # 🔹 Vérifier le groupe de l'utilisateur et rediriger
            if user.groups.filter(name="Admin").exists():
                return redirect('liste_employes')  # Admin → Employés
            elif user.groups.filter(name="Employe").exists():
                return redirect('liste_clients')  # Employé → Clients
            else:
                return redirect('liste_documents')  # Utilisateur standard → Documents
        
        else:
            messages.error(request, "Identifiants incorrects.")
    
    return render(request, 'gestion/connexion.html')


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.conf import settings
from .models import Employe, Client, Document
from .forms import EmployeForm, ClientForm, DocumentForm
import os


# ==========================
# 🔹 Vues pour les Employés
# ==========================

@login_required
@permission_required('gestion.view_employe', raise_exception=True)
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'gestion/liste_employes.html', {'employes': employes})


@login_required
@permission_required('gestion.add_employe', raise_exception=True)
def ajouter_employe(request):
    if request.method == "POST":
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'employé a été ajouté avec succès !")
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    return render(request, 'gestion/ajouter_employe.html', {'form': form})


@login_required
@permission_required('gestion.change_employe', raise_exception=True)
def modifier_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    if request.method == "POST":
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, "L'employé a été modifié avec succès !")
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'gestion/modifier_employe.html', {'form': form})


@login_required
@permission_required('gestion.delete_employe', raise_exception=True)
def supprimer_employe(request, id):
    employe = get_object_or_404(Employe, id=id)
    employe.delete()
    messages.success(request, "L'employé a été supprimé avec succès.")
    return redirect('liste_employes')


# ==========================
# 🔹 Vues pour les Clients
# ==========================

@login_required
@permission_required('gestion.view_client', raise_exception=True)
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'gestion/liste_clients.html', {'clients': clients})


@login_required
@permission_required('gestion.add_client', raise_exception=True)
def ajouter_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client a été ajouté avec succès !")
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'gestion/ajouter_client.html', {'form': form})


@login_required
@permission_required('gestion.change_client', raise_exception=True)
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client a été modifié avec succès !")
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'gestion/modifier_client.html', {'form': form})


@login_required
@permission_required('gestion.delete_client', raise_exception=True)
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    messages.success(request, "Le client a été supprimé avec succès.")
    return redirect('liste_clients')


# ==========================
# 🔹 Vues pour les Documents
# ==========================

@login_required
@permission_required('gestion.view_document', raise_exception=True)
def liste_documents(request):
    documents = Document.objects.all()
    return render(request, 'gestion/liste_documents.html', {'documents': documents})


@login_required
@permission_required('gestion.add_document', raise_exception=True)
def ajouter_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le document a été ajouté avec succès !")
            return redirect('liste_documents')
    else:
        form = DocumentForm()
    return render(request, 'gestion/ajouter_document.html', {'form': form})


@login_required
@permission_required('gestion.delete_document', raise_exception=True)
def supprimer_document(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()
    messages.success(request, "Le document a été supprimé avec succès.")
    return redirect('liste_documents')


# 🔹 Téléchargement sécurisé des fichiers
@login_required
@permission_required('gestion.view_document', raise_exception=True)
def telecharger_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    file_path = os.path.join(settings.MEDIA_ROOT, document.fichier.name)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


# ==========================
# 🔹 Authentification avec Redirection Dynamique
# ==========================

def connexion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('home')  # 🔹 Rediriger vers la page d'accueil après connexion
        else:
            messages.error(request, "Identifiants incorrects.")
    
    return render(request, 'gestion/connexion.html')

@login_required
def deconnexion(request):
    messages.success(request, "Vous avez été déconnecté avec succès.")
    logout(request)
    return redirect('connexion')

@login_required
def home(request):
    user = request.user

    # Déterminer le rôle de l'utilisateur pour adapter l'affichage
    if user.groups.filter(name="Admin").exists():
        role = "Admin"
    elif user.groups.filter(name="Employe").exists():
        role = "Employé"
    else:
        role = "Utilisateur"

    return render(request, 'gestion/home.html', {'role': role})


def erreur_403(request, exception=None):
    return render(request, 'gestion/403.html', status=403)

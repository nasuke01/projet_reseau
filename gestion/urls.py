from django.urls import path
from . import views

urlpatterns = [
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:id>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:id>/', views.supprimer_employe, name='supprimer_employe'),

    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:id>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:id>/', views.supprimer_client, name='supprimer_client'),

    path('documents/', views.liste_documents, name='liste_documents'),
    path('documents/ajouter/', views.ajouter_document, name='ajouter_document'),
    path('documents/supprimer/<int:id>/', views.supprimer_document, name='supprimer_document'),
    path('documents/telecharger/<int:document_id>/', views.telecharger_document, name='telecharger_document'),

    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    
    path('', views.home, name='home'),

]

    
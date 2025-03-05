from django import forms
from .models import Employe, Client, Document

# Formulaire pour les employés
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = '__all__'

# Formulaire pour les clients
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2, 'cols': 40}),  
        }

# Formulaire pour les documents
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

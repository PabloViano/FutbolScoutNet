from django import forms
from django.core.exceptions import ValidationError
from sitio.models import Publicacion

class FormPublicacion(forms.ModelForm):
    class Meta:
       model = Publicacion
       fields = ['titulo', 'texto', 'fecha', 'verificado']
       widgets = {
           'fecha': forms.DateInput(attrs={'type': 'date'})
       }


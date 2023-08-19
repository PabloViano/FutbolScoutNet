from django import forms
from django.core.exceptions import ValidationError
from sitio.models import Publicacion, Usuario

class FormPublicacion(forms.ModelForm):
    class Meta:
       model = Publicacion
       fields = ['titulo', 'texto', 'fecha', 'verificado']
       widgets = {
           'fecha': forms.DateInput(attrs={'type': 'date'})
       }

class PasswordField(forms.CharField):
    widget = forms.PasswordInput

class FormUsuario(forms.ModelForm):
    class Meta:
       model = Usuario
       fields = ['user name', 'email', 'password']
       widgets = {
           'email' : forms.EmailInput(),
           'password' : forms.PasswordInput()
       }
       
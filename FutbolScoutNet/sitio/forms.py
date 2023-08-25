from django import forms
from django.core.exceptions import ValidationError
from sitio.models import Post, Usuario

class FormPost(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['titulo', 'texto', 'fecha', 'verificado']
       widgets = {
           'fecha': forms.DateInput(attrs={'type': 'date'})
       }

class PasswordField(forms.CharField):
    widget = forms.PasswordInput

class FormUsuario(forms.ModelForm):
    class Meta:
       model = Usuario
       fields = ['username', 'email', 'password', 'posicion', 'nivel']
       widgets = {
           'email' : forms.EmailInput(),
           'password' : forms.PasswordInput()
       }
       
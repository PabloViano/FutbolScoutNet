from django import forms
from django.core.exceptions import ValidationError
from sitio.models import Post, Profile, Mensaje
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label = 'Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Repita Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_text = {'username': None,
            'email': None,}

class FormPost(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['titulo', 'texto', 'multimedia','video','verificado']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'posicion', 'nivel', 'edad']

from django import forms
from .models import Mensaje

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']  # Ajusta según tus necesidades

    def __init__(self, *args, emisor=None, receptor=None, **kwargs):
        super(MensajeForm, self).__init__(*args, **kwargs)
        self.emisor = emisor
        self.receptor = receptor

    def save(self, commit=True):
        mensaje = super(MensajeForm, self).save(commit=False)
        mensaje.emisor = self.emisor
        mensaje.receptor = self.receptor

        if commit:
            mensaje.save()

        return mensaje

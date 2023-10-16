from django import forms
from django.core.exceptions import ValidationError
from sitio.models import *
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
       fields = ['titulo', 'texto', 'multimedia','video']

class FormComment(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ['texto']   

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'posicion', 'nivel', 'edad']

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['texto']
        labels = {
            'texto': 'Mensaje',
        }


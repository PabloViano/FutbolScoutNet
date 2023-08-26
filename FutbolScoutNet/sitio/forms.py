from django import forms
from django.core.exceptions import ValidationError
from sitio.models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistretionForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label = 'Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Repita Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_text = {k:"" for k in fields}

class FormPost(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['titulo', 'texto', 'fecha', 'verificado']
       widgets = {
           'fecha': forms.DateInput(attrs={'type': 'date'})
       }

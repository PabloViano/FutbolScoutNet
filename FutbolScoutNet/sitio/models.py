from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    verificado = models.BooleanField(default=False)

class Usuario(models.Model):
    username = models.CharField(max_length=150)  # Asegúrate de definir la longitud máxima
    email = models.CharField(max_length=254)     # Asegúrate de definir la longitud máxima
    password = models.CharField(max_length=128)  # Asegúrate de definir la longitud máxima
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Solo crea el usuario si el objeto aún no tiene una clave primaria
            user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
            user.save()
        super().save(*args, **kwargs)

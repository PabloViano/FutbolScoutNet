from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    verificado = models.BooleanField(default=False)

class Usuario(models.Model):
    user = User.objects.create_user(models.CharField(max_lenght=10)   #Nombre usuario
                                    ,models.CharField(max_lenght=10)  #email
                                    ,models.CharField(max_lenght=10)) #contraseña
    user.save()


from django.db import models
from django.contrib.auth.models import User

class Posicion(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True, blank = True)
    image = models.ImageField(default='user.png')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',null = True, blank = True)
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    verificado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Post: {self.titulo[:20]} de {self.user.username}'

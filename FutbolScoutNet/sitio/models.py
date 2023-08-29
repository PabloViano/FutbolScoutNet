from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',null = True, blank = True)
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    multimedia = models.ImageField(upload_to="UsersMultimedia", null = True)
    verificado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Post: {self.titulo[:20]} de {self.user.username}'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
post_save.connect(create_profile, sender=User)
from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    username = models.CharField(max_length=150)  # Asegúrate de definir la longitud máxima
    email = models.CharField(max_length=254)     # Asegúrate de definir la longitud máxima
    password = models.CharField(max_length=128)  # Asegúrate de definir la longitud máxima
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Solo crea el usuario si el objeto aún no tiene una clave primaria
            user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
            user.save()
        super().save(*args, **kwargs)
# Create your models here.
class Profile(models.Model):
    user = user = models.ForeignKey(User, on_delete=models.CASCADE,null = True, blank = True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',null = True, blank = True)
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    verificado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Post: {self.titulo[:20]} de {self.user.username}'

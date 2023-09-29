from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import boto3

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
    image = models.ImageField(upload_to="Profiles_Images", default='user.png')
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)
        
    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

class Relationship(models.Model):
    from_user = models.ForeignKey(User,related_name='relationships',on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
    
    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user',]),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user',null = True, blank = True)
    post = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    fecha = models.DateTimeField(default=timezone.now)
    texto = models.CharField(max_length=500)

    def __str__(self):
        return f'Comentario del post {self.post.__str__} de {self.user.username}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',null = True, blank = True)
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField(default=timezone.now)
    multimedia = models.ImageField(upload_to="UsersMultimedia",blank = True, null = True)
    video = models.FileField(upload_to="videos",blank = True,null = True)
    verificado = models.BooleanField(default=False)
    comentarios = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment',null = True, blank = True)

    def __str__(self):
        if self.user:
            return f'Post: {self.titulo[:20]} de {self.user.username}'
        else:
            return f'Post: {self.titulo[:20]} (Usuario no especificado)'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
post_save.connect(create_profile, sender=User)
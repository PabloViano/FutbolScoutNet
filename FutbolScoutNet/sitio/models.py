from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="Profiles_Images", default='user.png')
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=50, default='activo')
    permitir_mensajes_de_desconocidos = models.BooleanField(default=True)
    
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
    from_user = models.ForeignKey(User, related_name='relationships_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='relationships_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user']),
        ]

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    post = models.ForeignKey('Post', on_delete=models.DO_NOTHING, related_name='comments', null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    texto = models.CharField(max_length=500)
    estado = models.CharField(max_length=50, default='publicada')

    def __str__(self):
        return f'Comentario del post {self.post} de {self.user.username}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField(default=timezone.now)
    multimedia = models.ImageField(upload_to="UsersMultimedia", blank=True, null=True)
    video = models.FileField(upload_to="videos", blank=True, null=True)
    estado = models.CharField(max_length=50, default='publicada')

    def get_comments(self):
        return Comment.objects.filter(post=self)

    def __str__(self):
        if self.user:
            return f'Post: {self.titulo[:20]} de {self.user.username}'
        else:
            return f'Post: {self.titulo[:20]} (Usuario no especificado)'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)

class Conversacion(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones_uno', null=True, blank=True)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones_dos', null=True, blank=True)

class Mensaje(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes', null=True, blank=True)
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, null=True, blank=True)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField(default=timezone.now)

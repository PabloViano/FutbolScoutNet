from django.db import models

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    verificado = models.BooleanField(default=False)



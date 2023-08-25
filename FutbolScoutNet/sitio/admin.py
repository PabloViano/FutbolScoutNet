from django.contrib import admin
from .models import Post, Profile, Posicion, Nivel

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Posicion)
admin.site.register(Nivel)
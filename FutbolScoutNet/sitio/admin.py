from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Posicion)
admin.site.register(Nivel)
admin.site.register(Relationship)
admin.site.register(Comment)
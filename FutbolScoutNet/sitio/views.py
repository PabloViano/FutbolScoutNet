from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from sitio.forms import FormPublicacion, FormUsuario
from sitio.models import Publicacion, Usuario

def inicio(request):
    return render(request, 'inicio.html', {})

def form_registro(request):
    if request.method == "POST":
        form = FormUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/feed")
    else:
        form = FormUsuario()

    return render(request, 'registro.html', {'form_registro': form })

@login_required
def form_publicacion(request):
    if request.method == "POST":
        form = FormPublicacion(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/feed")
    else:
        form = FormPublicacion()

    return render(request, 'publicacion.html', {'form_publicacion': form})

@login_required
def feed(request):
    publicaciones = Publicacion.objects.order_by("fecha")
    return render(request, 'feed.html',{'lista_publicaciones': publicaciones})

from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from sitio.forms import FormPublicacion
from sitio.models import Publicacion

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html', {})

def form_publicacion(request):
    if request.method == "POST":
        form = FormPublicacion(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/inicio")
    else:
        form = FormPublicacion()

    return render(request, 'publicacion.html', {'form_publicacion': form})
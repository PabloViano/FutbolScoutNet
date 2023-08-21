from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sitio.forms import FormPublicacion, FormUsuario
from sitio.models import Publicacion
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

def inicio(request):
    return render(request, 'inicio.html', {})

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        return "/"

class CustomLoginView(LoginView):
    def get_success_url(self):
        return "/"

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

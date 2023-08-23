from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sitio.forms import FormPost, FormUsuario
from sitio.models import Post

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
def form_post(request):
    if request.method == "POST":
        form = FormPost(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/feed")
    else:
        form = FormPost()

    return render(request, 'post.html', {'form_post': form})

@login_required
def feed(request):
    posts = Post.objects.order_by("fecha")
    return render(request, 'feed.html',{'lista_posts': posts})
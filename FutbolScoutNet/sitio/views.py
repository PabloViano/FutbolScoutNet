from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from sitio.forms import FormPost, UserRegistretionForm
from sitio.models import Post, Profile, User

def inicio(request):
    return render(request, 'inicio.html', {})

def registro(request):
    if request.method == "POST":
        form = UserRegistretionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = UserRegistretionForm()

    return render(request, 'registro.html', {'form_registro': form })

@login_required
def form_post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        form = FormPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            form.save()
            return redirect("/feed")
    else:
        form = FormPost()

    return render(request, 'post.html', {'form_post': form})

@login_required
def feed(request):
    posts = Post.objects.order_by("fecha")
    return render(request, 'feed.html',{'lista_posts': posts})

@login_required
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
        usuario = User.objects.get(username=username)
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'profile.html', {'user':user, 'posts':posts})

@login_required
def listado_perfiles(request):
    perfiles = Profile.objects.order_by()
    return render(request, 'listado_perfiles.html', {'lista_perfiles':perfiles})
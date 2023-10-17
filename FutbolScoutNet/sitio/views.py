from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from sitio.forms import *
from sitio.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from sitio.token import account_activation_token
from django.views.decorators.http import require_GET
from haystack.query import SearchQuerySet
from django.db.models import Q, OuterRef, Subquery
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

def inicio(request):
    return render(request, 'inicio.html', {})

def registro(request):
    # if request.method == "POST":
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login')
    # else:
    #     form = UserRegistrationForm()

    # return render(request, 'registro.html', {'form_registro': form })
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(request,template_name="registro.html",context={"form_registro": form})

@login_required
def conversaciones(request):
    # Subconsulta para obtener el último mensaje de cada conversación
    subquery = Mensaje.objects.filter(conversacion=OuterRef('pk')).order_by('-fecha').values('texto')[:1]

    conversaciones = Conversacion.objects.annotate(
        ultimo_mensaje=Subquery(subquery)
    ).filter(
        Q(emisor=request.user) | Q(destinatario=request.user)
    ).exclude(
        Q(emisor=request.user, destinatario=request.user)
    )

    return render(request, 'conversaciones.html', {'conversaciones': conversaciones})


@login_required
def mensajes(request, username):
    # Intenta obtener la conversación existente o crea una nueva
    conversacion = Conversacion.objects.filter(
        Q(emisor=request.user, destinatario__username=username) |
        Q(destinatario=request.user, emisor__username=username)
    ).first()

    if conversacion is None:
        conversacion = Conversacion.objects.create(
            emisor=request.user,
            destinatario=get_object_or_404(User, username=username)
        )

    # Obtener todos los mensajes asociados a la conversación
    mensajes = Mensaje.objects.filter(conversacion=conversacion)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            nuevo_mensaje = form.save(commit=False)
            nuevo_mensaje.user = request.user
            nuevo_mensaje.conversacion = conversacion
            nuevo_mensaje.save()
            return redirect('mensajes', username=username)
    else:
        form = MensajeForm()

    return render(request, 'mensajes.html', {'conversacion': conversacion, 'mensajes': mensajes, 'form': form})

@login_required
def form_post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        form = FormPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            form.save()
            return redirect("/feed")
    else:
        form = FormPost()

    return render(request, 'post.html', {'form_post': form})

def feed(request):
    posts_per_page = 10
    if request.user.is_anonymous:
        all_posts = Post.objects.all().order_by('-fecha')
        paginator = Paginator(all_posts, posts_per_page)
        followed_posts = None
        comments = Comment.objects.filter(post__in=all_posts)
    else:
        current_user = request.user

        followed_users = Relationship.objects.filter(from_user=current_user)
        followed_posts = Post.objects.filter(user__in=followed_users.values('to_user')).order_by('-fecha')
        all_posts = Post.objects.all().order_by('-fecha')
        paginator = Paginator(all_posts, posts_per_page)

        # Obtener los comentarios para todas las publicaciones
        comments = Comment.objects.filter(post__in=all_posts)

    # Verifica si se realizó una búsqueda
    search_query = request.GET.get('search', '')

    if search_query:
        # Realiza una búsqueda utilizando Haystack
        search_results = SearchQuerySet().filter(content=search_query)
        search_posts = [result.object for result in search_results]
        if not request.user.is_anonymous:
            # Filtra los resultados de búsqueda para mostrar solo los posts seguidos
            search_posts_followed = [post for post in search_posts if post in followed_posts]
    else:
        search_posts = []
        search_posts_followed = []

    return render(request, 'feed.html', {
        'followed_posts': followed_posts,
        'all_posts': paginator.page(1),
        'search_posts': search_posts,  # Agrega los resultados de búsqueda a la plantilla
        'search_posts_followed': search_posts_followed,
        'comments': comments,
        'search_query': search_query,  # Pasa la consulta de búsqueda a la plantilla
    })

def load_more_posts(request):
    page = request.GET.get('page')
    posts_per_page = 10  # Cantidad de publicaciones por página

    all_posts = Post.objects.all().order_by('-fecha')

    paginator = Paginator(all_posts, posts_per_page)
    try:
        page_posts = paginator.page(page)
    except EmptyPage:
        return JsonResponse()  # Devuelve una respuesta vacía cuando no hay más páginas

    context = {
        'posts': page_posts,
    }

    if page == '1':
        # Si es la primera página, muestra solo los primeros 10 posts
        context['posts'] = page_posts[0:10]

    return render(request, 'post_partial.html', context)

# Crea una plantilla parcial 'post_partial.html' para renderizar las publicaciones adicionales
# Esta plantilla debería ser similar a la parte de tu feed.html que muestra una sola publicación

@login_required
def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    profile = Profile.objects.get(user=user)
    followers = Relationship.objects.filter(to_user=User.objects.get(username=username)).count()
    return render(request, 'profile.html', {'user':user, 'posts':posts, 'profile':profile, 'followers': followers})

@login_required
def profile_edit(request, username=None):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    # Verificar que el usuario actual esté editando su propio perfil
    if request.user != user:
        return redirect('profile', username=username)

    if request.method == "POST":
        form = ProfileEditForm(request.POST,  request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

@login_required
def listado_perfiles(request):
    perfiles = Profile.objects.filter()
    niveles = Nivel.objects.all()
    posiciones = Posicion.objects.all()

    # Obtener los parámetros de filtrado de la solicitud GET
    edad_min = request.GET.get('edad_min')
    edad_max = request.GET.get('edad_max')
    nivel = request.GET.get('nivel')
    posicion = request.GET.get('posicion')

    # Aplicar filtros si los parámetros están presentes
    if edad_min:
        perfiles = perfiles.filter(edad__gte=edad_min)
    if edad_max:
        perfiles = perfiles.filter(edad__lte=edad_max)
    if nivel:
        perfiles = perfiles.filter(nivel__nombre=nivel)
    if posicion:
        perfiles = perfiles.filter(posicion__nombre=posicion)

    return render(request, 'listado_perfiles.html', {'lista_perfiles': perfiles, 'user': request.user, 'niveles':niveles, 'posiciones':posiciones})

@login_required
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username = username)
    to_user_id = to_user
    if (not Relationship.objects.filter(from_user = current_user.id, to_user=to_user_id).exists()):
        rel = Relationship(from_user=current_user, to_user=to_user_id)
        rel.save()
    return redirect('profile', username=to_user.username)

@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username = username)
    to_user_id = to_user
    if (Relationship.objects.filter(from_user = current_user.id, to_user=to_user_id).exists()):
        rel = Relationship.objects.filter(from_user = current_user.id, to_user=to_user_id).get()
        rel.delete()
    return redirect('profile', username=to_user.username)

#EMIAL CONFIRMATION

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('/accounts/login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@login_required
def form_comment(request, post_id):
    current_user = get_object_or_404(User, pk=request.user.pk)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = FormComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.post = post  # Asociar el comentario al post correspondiente
            form.save()
            return redirect("/feed")
    else:
        form = FormComment()

    return render(request, 'comment.html', {'form_comment': form})

@require_GET
def robots_txt(request):
    return HttpResponse(content_type="text/plain")

def rebuild_index(request):
    from django.core.management import call_command
    from django.http import JsonResponse
    try:
        call_command("rebuild_index", noinput=False)
        result = "Index rebuilt"
    except Exception as err:
        result = f"Error: {err}"

    return JsonResponse({"result": result})
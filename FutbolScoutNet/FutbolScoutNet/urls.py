"""
URL configuration for FutbolScoutNet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from sitio import views
from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.inicio, name = "home"),
    path('', views.inicio, name = "landing_page"),
    path('publicacion/', views.form_post),
    path("accounts/", include("django.contrib.auth.urls")),
    path('feed/', views.feed),
    path('registro/', views.registro),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('listado-perfiles/', views.listado_perfiles),
    path('follow/<str:username>/', views.follow, name="follow"),
    path('unfollow/<str:username>/', views.unfollow, name="unfollow"),
    path('profile-edit/<str:username>/', views.profile_edit),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
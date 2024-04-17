"""
URL configuration for library_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('library_app.urls')),
    path('logout/', include('library_app.urls')),
    path('clientes/', include('library_app.urls')),
    path('cliente/novo', include('library_app.urls')),
    path('cliente/editar/<int:id>/', include('library_app.urls')),
    path('cliente/remover/<int:id>/', include('library_app.urls')),
    path('', include('library_app.urls')),
    path('', RedirectView.as_view(url='login/', permanent=True)),  # Redireciona a raiz para /login/
]

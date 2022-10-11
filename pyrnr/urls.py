"""pyrnr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from pages.views import scriptdash_view, runner_view, saver_view, home_view, register_view, newscript_view, deleter_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('scripts/', scriptdash_view, name='scriptdash'),
    path('scripts/new', newscript_view, name='new_script'),
    path('', home_view, name='home'),
    path('runner', runner_view, name='runner'),
    path('saver', saver_view, name='saver'),
    path('register', register_view, name='register'),
    path('deleter', deleter_view, name='deleter'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

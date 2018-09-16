"""eedf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, re_path
from modulevieasso import views

urlpatterns = [
    # path('admin/', admin.site.urls,name='admin'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('editcr/', views.edit, name='editcr'),
    path('docs/', views.docs, name='docs'),
    path('listemargement/', views.listemargement, name='listemargement'),
    path('listcr/', views.listcr, name='listcr'),
    path('parametre/', views.parametre, name='parametre'),
    path('nomination/', views.nominationredacteur, name='nomination'),
    path('listnomination/', views.listnomination, name='listnomination'),
    path('out/', views.sortir, name='logout'),
    path('validernomination/', views.validernomination, name='validernomination'),
    path('saveanimationteam/', views.saveanimationteam, name='saveanimationteam'),
    path('removenomination/', views.removenomination, name='removenomination'),
    path('', views.index, name='index'),
    re_path(r'.', views.index, name="any"),
]

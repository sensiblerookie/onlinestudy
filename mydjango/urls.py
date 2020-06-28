"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from app import views
from user import userViews
from public import publicViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', userViews.login),
    path('login/', userViews.login),
    path('logout/', userViews.logout),
    path('register/', userViews.register),
    path('registration/', userViews.register),
    path('profile/', userViews.profile),
    path('index/', views.index),
    path('home/', views.home),
    path('custom_home/', views.custom_home),
    path('result/', views.result),
    path('result_class/', views.result_class),
    path('title_add/', views.title_add),
    path('basetop/', publicViews.basetop),
    path('basebottom/', publicViews.basebottom),
    path('base/', publicViews.base),
    path('accounts/login/', userViews.login),
]

"""Satway2 URL Configuration

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
from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('profile/', views.viewProfile, name= "viewProfile"),
    path('login/', views.loginUser, name= "loginPage"),
    path('logout/', views.logoutUser, name= "logoutPage"),
    path('changepassword/',views.changePassword, name= "changePassword"),
    path('resetPassword/',views.resetPassword,name="resetPassword"),
    path('profile/', views.viewProfile, name="Profile")

]

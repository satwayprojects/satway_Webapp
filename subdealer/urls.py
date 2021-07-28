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
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'subdealer'

urlpatterns = [
    path('dashboard/', views.dashboard, name= "Dashboard"),
    path('userregisteration/', views.userRegisteration, name="userRegisteration"),
    path('deviceallocation/user/', views.deviceAllocationUser, name="deviceAllocationUser"),
    path('reallocation/',views.reallocateDevice, name="reallocateDevice"),
    path('inventory',views.inventory,name = "inventory"),
    path('transactionsearch',views.transactionsearch,name = "transactionsearch"),
    path('ajax_password_reset',views.ajax_password_reset, name="ajax_password_reset"),
    path('ajax_load_user',views.ajax_load_user,name = "ajax_load_user"),
    path('inventory_sold',views.inventory_sold,name = "inventory_sold"),
    path('inventory_active',views.inventory_active,name = "inventory_active"),
    path('inventory_deactive',views.inventory_deactive,name = "inventory_deactive"),

    path('editprofile',views.editprofile,name = "editprofile"),
    path('profile',views.change_password,name = "profile"),

    path('inventory_sold',views.inventory_sold,name = "inventory_sold"),
    path('inventory_active',views.inventory_active,name = "inventory_active"),
    path('inventory_deactive',views.inventory_deactive,name = "inventory_deactive"),

]

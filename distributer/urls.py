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

app_name = 'distributer'

urlpatterns = [
    path('dashboard/', views.dashboard, name= "Dashboard"),
    path('dealerregisteration/', views.dealerRegisteration, name="dealerRegisteration"),
    path('userregisteration/', views.userRegisteration, name="userRegisteration"),
    # path('allocation/distributer/', views.distributerAllocation, name="distributerAllocation"),
    # path('allocation/user/', views.userAllocation, name="userAllocation"),
    path('deviceallocation/dealer/', views.deviceAllocationDealer, name="deviceAllocationDealer"),
    path('deviceallocation/user/', views.deviceAllocationUser, name="deviceAllocationUser"),
    path('deviceallocation/loadUser',views.loadUser,name = "loadDistributer"),
    path('deviceallocation/checkusernamevalid',views.checkusernamevalid,name = "bulkadd"),
    path('deviceallocation/allocationimeiCheck',views.allocationimeiCheck,name = "allocationimeiCheck"),
    path('reallocation/',views.reallocateDevice, name="reallocateDevice"),
    path('inventory',views.inventory,name = "inventory"),

    path('ajax_password_reset',views.ajax_password_reset, name="ajax_password_reset"),
    path('ajax_load_user',views.ajax_load_user,name = "ajax_load_user"),
    path('ajax_load_dealer',views.ajax_load_dealer,name = "ajax_load_dealer"),
  
    path('editprofile',views.editprofile,name = "editprofile"),
    path('profile',views.change_password,name = "profile"),

    path('ajax_password_reset',views.ajax_password_reset, name="ajax_password_reset"),
    path('ajax_load_user',views.ajax_load_user,name = "ajax_load_user"),
    path('ajax_load_dealer',views.ajax_load_dealer,name = "ajax_load_dealer"),
    path('inventory_sold',views.inventory_sold,name = "inventory_sold"),
    path('inventory_active',views.inventory_active,name = "inventory_active"),
    path('inventory_deactive',views.inventory_deactive,name = "inventory_deactive"),
    path('inventory_dealer',views.inventory_dealer,name = "inventory_dealer"),
    path('inventory_deactive_stock',views.inventory_deactive_stock,name = "inventory_deactive_stock"),
    path('inventory_deactive_sold',views.inventory_deactive_sold,name = "inventory_deactive_sold"),
    path('certificate',views.certificate,name = 'certificate'),

]

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

app_name = 'user'

urlpatterns = [
    path('dashboard/', views.dashboard, name= "Dashboard"),
    path('subuserregisteration/', views.subUserRegisteration, name = "subUserRegisteration"),
    path('vehicles/', views.allVehicles, name ="Vehicles"),
    path('allocation/',views.allocateSubUser, name ="allocateSubUser"),

    path('load_live_view',views.load_live_view,name = "load_live_view"),
    path('editprofile',views.editprofile,name = "editprofile"),
    path('profile',views.change_password,name = "profile"),
    path('load_history',views.load_history,name = "load_history"),

    path('load_history_view',views.history_live_view,name = "history_live_view"),
    path('ajax_load_live',views.ajax_load_live,name="ajax_load_live"),

    path('ajax_load_live',views.ajax_load_live,name="ajax_load_live"),
    path('ajax_fetch_graphs_data',views.ajax_fetch_graphs_data,name = "ajax_fetch_graphs_data"),
    path('ajax_vehicle_no_load',views.ajax_vehicle_no_load,name = "ajax_vehicle_no_load"),
    
    path('allocationstatus/',views.allocationstatus,name='allocationstatus'),
    path('loadvehicle/',views.loadvehicle,name='ajax_load_vehicle'),

    path('loadsubuser',views.load_subuser,name='load_subuser'),
    path('passwordreset',views.password_reset,name="ajax_password_reset"),
    path('load_subuser_phone',views.load_subuser_phone, name="load_subuser_phone"),
    path('load_vehicle_no',views.load_vehicle_no, name="load_vehicle_no"),

    path('checkvehicleno',views.check_vehicleno,name="check_vehicle_no"),
    path('loadvehiclesubuser',views.load_vehicle_subuser,name="load_vehicle_subuser"),

    path('reallocation',views.reallocation,name='reallocation'),
    path('reallocatevehicle',views.rellocatevehicle,name="reallocate_vehicle"),
    path('deletesubuser',views.delete_subuser,name="DeleteSubUser"),

]

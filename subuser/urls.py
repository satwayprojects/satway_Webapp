from django.contrib import admin
from django.urls import path
from . import views

app_name = 'subuser'

urlpatterns = [
    path('dashboard/', views.dashboard, name= "Dashboard"),
    path('vehicles/', views.allVehicles, name ="Vehicles"),
    path('load_live_view',views.load_live_view,name = "load_live_view"),
    path('editprofile',views.editprofile,name = "editprofile"),

    path('ajax_load_live',views.ajax_load_live,name="ajax_load_live"),
    path('ajax_vehicle_no_load',views.ajax_vehicle_no_load,name = "ajax_vehicle_no_load"),
    path('ajax_fetch_graphs_data',views.ajax_fetch_graphs_data,name = "ajax_fetch_graphs_data"),
]
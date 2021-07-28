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

app_name = 'index'

urlpatterns = [
    path('', views.loginUser, name= "loginPage"),
    path('loadUser',views.loadUser,name = "ajax_loadUser"),
    path('allocationimeicheck',views.allocationimeiCheck,name = "ajax_allocationImeiCheck"),
    path('checkDeallocationStatus',views.checkReallocationStatus,name = "checkReallocationStatus"),
    path('ajax_check_user_username/', views.ajax_check_user_username, name='ajax_check_user_username'),
    path('loadimei/',views.ajax_load_user_imei ,name='ajax_load_user_imei'),

    path('forgotpassword/', views.forgot_password, name= "forgot_password"),

    path('ajax_loaddealer/',views.ajax_loaddealer ,name='ajax_loaddealer'),
    path('ajax_loaddealer_users/',views.ajax_loaddealer_users ,name='ajax_loaddealer_users'),
    path('ajax_loaddealer_subdealer/',views.ajax_loaddealer_subdealer ,name='ajax_loaddealer_subdealer'),
    
    path('ajax_check_subuser_name',views.ajax_check_subuser_name, name='ajax_check_sub_username'),
    path('cetificate',views.cetificate,name = 'cetificate'),
]
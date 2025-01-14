"""Product service URL Configuration

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
from django.urls import include
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.conf import settings    
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.product_login, name = 'product_login'),
    path('logout/', views.product_logout, name = 'product_logout'),
    path('signup/', views.product_signup, name = 'product_signup'),
    path('login_redirect/', views.product_login_redirect, name = 'product_login_redirect'),
    # path('check_login/', views.check_login, name = 'check_login'),
    path('owns/<str:product_name>', views.owns, name = 'owns_product'),
    path('register/', views.register, name = 'register_product'),
    path('registration_done/', views.registration_done, name = 'registration_done'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit-username', views.edit_username, name='edit_username'),
    path('profile/serial_keys/', views.get_serial_list, name='get_serial_list'),
    path('transmit_serial/<str:serial_key>', views.transmit_serial, name='transmit_serial'),
    
    #this is for react
    path('get_plans/', views.get_plans, name="get_plans"),
    path('get_plan/<str:plan_id>', views.get_plan, name="get_plan"),
    path('get_cards/', views.get_cards, name="get_cards"),
]

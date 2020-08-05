from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url('add-resin/', views.add_resinInfo),
    url('add-serial/', views.add_serial)
]

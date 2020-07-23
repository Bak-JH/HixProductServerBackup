from django.conf.urls import url
from django.contrib import admin
from management.views import add_resinInfo

urlpatterns = [
    url('add-resin/', add_resinInfo)
]

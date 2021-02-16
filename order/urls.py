from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe),
    path('cancel/<str:billing_id>', views.cancel_payment),
]

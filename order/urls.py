from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.subscribe),
    path('cancel/<str:receipt_id>', views.cancel_payment),
    path('thank-you', TemplateView.as_view(template_name="order/thank_you.html")),
]

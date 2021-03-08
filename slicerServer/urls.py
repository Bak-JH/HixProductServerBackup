"""slicerServer URL Configuration

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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls
from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('management.urls')),
    path('accounts/', include('allauth.urls')), 
    path('', TemplateView.as_view(template_name="slicerServer/index.html")),
    path('privacy', TemplateView.as_view(template_name="slicerServer/privacypolicy.html")),
    path('terms', TemplateView.as_view(template_name="slicerServer/termsofservice.html")),
    path('product/', include('product.urls')),
    path('resin/', include('resin.urls')),
    path('setup/', include('setup.urls')),
    path('post/', include('posts.urls')),
    path('email/', include(mail_urls)),
    path('order/', include('order.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
]


#static stuff
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>', views.view_post, name = 'view_post'),
    path('edit', views.create_post, name = 'create_post'),
    path('', views.post_list, name = 'post_list'),
]

from django.urls import path
from . import views

urlpatterns = [
    #url('add-resin/', views.add_resinInfo),
    path('add-serial/', views.add_serial),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view()),
]

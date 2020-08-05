from django.urls import path

from . import views

urlpatterns = [
	# path('get_csrf/', views.get_csrf),
	path('update/<str:printer_name>',views.update_check,name='update_check'),
	path('download/<str:printer_name>',views.download_all,name='download_all'),
]


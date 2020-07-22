from django.urls import path

from . import views

urlpatterns = [
	# path('get_csrf/', views.get_csrf),
	path('test/',views.test),
	path('update/',views.update_check,name='update_check'),
	path('download/',views.download_all,name='download_all'),
	path('download/<slug:materialName>/',views.download,name='download'),
]


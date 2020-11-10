from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('authentication/', views.authentication, name='authentication'),
	path('base/', views.base, name='base'),
	path('profile/', views.profile, name='profile'),
	path('dashboard/', views.dashboard, name='dashboard'),
	url(r'dataset/(?P<name>[a-zA-Z0-9_-]+?)/', views.specificDataset, name='dataset'),
	path('logout/', views.logout, name='logout'),
	path('', views.index, name="index"),
	path('request/', views.datasetRequestPage, name="datasetRequestPage"),
	path('gdrive/', views.gDriveAPI, name="gdrive"),
]
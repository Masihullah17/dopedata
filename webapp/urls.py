from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name="landingPage"),
	path('authentication/', views.authentication, name='authentication'),
	path('resetpassword/', views.resetPassword, name='resetpassword'),
	path('base/', views.base, name='base'),
	path('profile/', views.profile, name='profile'),
	path('dashboard/', views.dashboard, name='dashboard'),
	url(r'dataset/(?P<uid>[a-zA-Z0-9_-]+?)/', views.specificDataset, name='dataset'),
	path('logout/', views.logout, name='logout'),
	path('index/', views.index, name="index"),
	path('request/', views.datasetRequestPage, name="datasetRequestPage"),
	path('gdrive/', views.gDriveAPI, name="gdrive"),
]
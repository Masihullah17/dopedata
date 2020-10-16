from django.urls import include, path
from . import views

urlpatterns = [
	path('auth/', views.auth, name='auth'),
	path('signup/', views.signup, name='signup'),
	path('logout/', views.logout, name='logout'),
	path('', views.index, name="index"),
]
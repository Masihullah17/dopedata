from django.urls import path
from data.api import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url

urlpatterns = [
	path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
	url(r'users/(?P<username>[a-zA-Z0-9@._-]+?)/', views.userProfile, name='user_profile_api'),
	url(r'search/(?P<datasetName>[a-zA-Z0-9 _-]+?)/', views.datasetSearch, name='dataset_search_api'),
]
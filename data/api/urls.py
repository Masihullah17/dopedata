from django.urls import path
from data.api import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url

urlpatterns = [
	# path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
	url(r'users/(?P<username>[a-zA-Z0-9@._-]+?)/', views.userProfile, name='user_profile_api'),
	url(r'search/(?P<datasetName>[a-zA-Z0-9 _-]+?)/', views.datasetSearch, name='dataset_search_api'),
	url(r'request/$', views.requestDataset, name='request_dataset_post'),
	url(r'request/(?P<requestId>[a-zA-Z0-9 _-]+?)/$', views.requestDataset, name='request_dataset'),
	url(r'contribute/$', views.contribution, name='contribution_post'),
	url(r'contribute/(?P<contributionId>[a-zA-Z0-9 _-]+?)/$', views.contribution, name='contribution'),
	url(r'download/(?P<requestId>[a-zA-Z0-9 _-]+?)/$', views.downloadDataset, name='download'),
]

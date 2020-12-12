from django.urls import include, path
from . import views

urlpatterns = [
	path('contribute/',views.contribute, name="contribute_view"),
	path('profile/',views.userProfile, name="user_profile_view"),
	path('search/',views.search, name="search_view"),
	path('request/',views.requestpage, name="request_view"),
]
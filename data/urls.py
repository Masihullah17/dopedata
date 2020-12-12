from django.urls import include, path
from . import views

urlpatterns = [
	path('api/', include('data.api.urls')),
]

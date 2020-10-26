# Django Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

# Python Imports
import json

# Model Imports
from data.models import UserProfile, Datasets

@api_view(http_method_names=['GET',])
@permission_classes([IsAuthenticated])
def userProfile(request, username):
	try:
		userDetails = UserProfile.objects.get(email=username)
		serializedData = serializers.serialize('python', [userDetails, ])
		return HttpResponse(json.dumps(serializedData[0]['fields'], cls=DjangoJSONEncoder), status=status.HTTP_200_OK, content_type='application/json')
	except UserProfile.DoesNotExist:
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

	
@api_view(http_method_names=['GET',])
@permission_classes([IsAuthenticated])
def datasetSearch(request, datasetName):
	try:
		datasetDetails = Datasets.objects.filter(dataset_name__icontains=datasetName)
		serializedData = serializers.serialize('python', datasetDetails)
		filteredDatasets = []
		for dataset in serializedData:
			filteredDatasets.append(dataset['fields'])
		
		return HttpResponse(json.dumps(filteredDatasets, cls=DjangoJSONEncoder), status=status.HTTP_200_OK, content_type='application/json')
	except UserProfile.DoesNotExist:
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)
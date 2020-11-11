# Django Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

# Python Imports
import json
import uuid

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
		datasetDetails = Datasets.objects.filter(dataset_name__icontains=datasetName, is_deleted=False)
		serializedData = serializers.serialize('python', datasetDetails)
		filteredDatasets = []
		for dataset in serializedData:
			filteredDatasets.append(dataset['fields'])
		
		if filteredDatasets == []:
			raise Datasets.DoesNotExist
		
		return HttpResponse(json.dumps(filteredDatasets, cls=DjangoJSONEncoder), status=status.HTTP_200_OK, content_type='application/json')
	except Datasets.DoesNotExist:
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=['POST', 'PUT', 'DELETE',])
@permission_classes([IsAuthenticated])
def requestDataset(request, requestId=''):
	if request.method == "POST":
		if requestId == '':
			return postRequestDataset(request)
		else:
			return triggerAcceptanceDataset(request, requestId)
	elif request.method == "PUT":
		return putRequestDataset(request, requestId)
	elif request.method == "DELETE":
		return deleteRequestDataset(request, requestId)

def postRequestDataset(request):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)
		uid = uuid.uuid1()
		dataset = Datasets.objects.create(dataset_name = request.data['dataset_name'],
								created_by = created_by,
								uid = uid,
								description = request.data['description'],
								usecase = request.data['usecase'],
								required_size = request.data['required_size'],
								entry_time = timezone.now(),
								data = json.dumps(request.data['data']),
								)
		dataset.save()

		return Response({"status" : "Successful", "request-id" : uid}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

def triggerAcceptanceDataset(request, requestId):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)

		dataset = Datasets.objects.get(uid = requestId, created_by = created_by, is_deleted=False)
		dataset.stop_accepting_contributions = not dataset.stop_accepting_contributions
		dataset.save()
	
		return Response({"Current Status" : "Accepting Contributions" if not dataset.stop_accepting_contributions else "NOT Accepting Contributions", "status" : "Triggered Successfully", "request-id" : requestId}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)	

def putRequestDataset(request, requestId):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)

		dataset = Datasets.objects.get(uid = requestId, created_by = created_by)
		dataset.dataset_name = request.data.get('dataset_name', dataset.dataset_name)
		dataset.description = request.data.get('description', dataset.description)
		dataset.usecase = request.data.get('usecase', dataset.usecase)
		dataset.required_size = request.data.get('required_size', dataset.required_size)
		dataset.data = json.dumps(request.data.get('data', json.loads(dataset.data)))
		dataset.entry_time = timezone.now()
		dataset.save()

		return Response({"status" : "Updated Successfully", "request-id" : requestId}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

def deleteRequestDataset(request, requestId):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)
		uid = uuid.uuid1()

		dataset = Datasets.objects.get(uid = requestId, created_by = created_by)
		dataset.is_deleted = True
		dataset.stop_accepting_contributions = True
		dataset.delete_uid = uid
		dataset.save()
	
		return Response({"status" : "Deleted Successfully", "deletion-reference-id" : uid}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)
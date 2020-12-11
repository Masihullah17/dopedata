# Django Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.conf import settings

# Python Imports
import json
import uuid
import os

# Model Imports
from data.models import UserProfile, Datasets, Contributions, FilesUploads

# Mapper, file type to name
filetype2Name = {"jpg" : "Image", "png" : "Image", "tif" : "Image", "jpeg" : "Image", 
					"mp4" : "Video", "mpeg" : "Video", "mkv" : "Video", "3gp" : "Video", 
					"mp3" : "Audio", "aac" : "Audio", "ogg" : "Audio"}

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

@api_view(http_method_names=['POST', 'DELETE',]) #'PUT',
@permission_classes([IsAuthenticated])
def contribution(request, contributionId=''):
	if request.method == "POST":
		return postContribution(request)
	elif request.method == "PUT":
		return putContribution(request, contributionId)
	elif request.method == "DELETE":
		return deleteContribution(request, contributionId)

def postContribution(request):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)
		uid = uuid.uuid1()
		time = timezone.now()

		# Check contribution data matches with request data
		print(request.POST)

		data = json.loads(request.data['data'])["data"]

		print(request.FILES)
		for name, mediaFile in request.FILES.items():
			fileSaved = FilesUploads.objects.create(uploaded_user=created_by, dataset_uid=request.POST['request-id'], contribution_id=uid, upload_time=time, uploaded_file=mediaFile)
			initial_path = fileSaved.uploaded_file.path
			fileSaved.uploaded_file.name = str(uid) + "_" + str(timezone.now().timestamp()).replace(".", "") + "." + initial_path.split(".")[-1]
			new_path = "./media/" + fileSaved.uploaded_file.name
			os.rename(initial_path, new_path)
			fileSaved.save()

			# Change data files content in json to path of file saved
			for answer in data:
				if name in list(answer.values()):
					try:
						filetype = filetype2Name[new_path.split(".")[-1]]
					except KeyError:
						filetype = "Other"
					answer[filetype] = "/media/" + fileSaved.uploaded_file.name

		contributionCreated = Contributions.objects.create(data = json.dumps(data),
													contributed_by=created_by,
													contribution_time=time,
													request_uid=request.data['request-id'],
													request_dataset=Datasets.objects.get(uid=request.data['request-id']),
													contribution_uid=uid,
													)
		contributionCreated.save()

		dataset = Datasets.objects.get(uid=request.data['request-id'])
		created_by.points += dataset.points
		
		if created_by.points > 20 and created_by.points < 50:
			created.badeges = ['bronze']
		elif created_by.points > 50 and created_by.points < 100:
			created_by.badges = ['bronze', 'silver']
		elif created_by.points > 100:
			created_by.badges = ['bronze', 'silver', 'gold']

		created_by.save()	

		return Response({"status" : "Successful", "contribution-id" : uid}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

def putContribution(request,contributionId):
	try:
		created_by = UserProfile.objects.get(name=request.user.first_name, email=request.user.username)

		dataset = Contributions.objects.get(uid = contributionId, created_by = created_by)
		dataset.data = json.dumps(request.data.get('data', json.loads(dataset.data)))
		dataset.contribution_time = timezone.now()
		dataset.save()
		return Response({"status" : "Updated Successfully", "contribution-id" : contributionId}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)

def deleteContribution(request, contributionId):
	try:
		uid = uuid.uuid1()

		contributed = Contributions.objects.get(contribution_uid=contributionId)
		contributed.deleted = True
		contributed.deletion_id = uid
		contributed.save()

		return Response({"status" : "Deleted Successfully", "deletion-id" : uid}, status=status.HTTP_200_OK)
	except Exception as e:
		print(e)
		data = {"status": "Not Found", "status-code": 404, "message": "Uh Oh! You fumbled on something !!"}
		return Response(data, status=status.HTTP_404_NOT_FOUND)
# Django imports
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse

# Python imports
import requests
import uuid
import json

# Model Imports
from data.models import UserProfile, Datasets

def signup(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get("pass")
		confirmPassword = request.POST.get("confirmPass")

		if password == confirmPassword:
			try:
				user = settings.FIREBASE_AUTH.create_user_with_email_and_password(email, password)
				user_entry = User.objects.create(first_name=name, username=email)
				user_entry.save()

				profile = UserProfile.objects.create(name=name, email=email, joined=timezone.now())
				profile.save()
				
				access_token = Token.objects.create(user=user_entry)

				return redirect("auth")

			except Exception as e:
				print(e)
				return render(request,"signup.html",{"error":e})

	return render(request, 'signup.html')

def auth(request):
	if request.method == 'POST':
		email=request.POST.get('email')
		passw = request.POST.get("pass")
		try:
			user = settings.FIREBASE_AUTH.sign_in_with_email_and_password(email,passw)
			user = settings.FIREBASE_AUTH.refresh(user['refreshToken'])
		except Exception as e:
			print(e)
			message = "invalid cerediantials"
			return render(request,"auth.html",{"msg":message})

		request.session['session_id'] = user['idToken']
		request.session['refreshToken'] = user['refreshToken']

		return redirect('index')
	
	return render(request, 'auth.html')

def logout(request):
	try:
		del request.session['session_id']
	except:
		pass
	return redirect("auth")

def index(request):
	if request.session.has_key('session_id'):
		try:
			username = settings.FIREBASE_AUTH.get_account_info(request.session['session_id'])['users'][0]['email']
		except requests.exceptions.HTTPError:
			user = settings.FIREBASE_AUTH.refresh(request.session['refreshToken'])
			request.session['session_id'] = user['idToken']
			request.session['refreshToken'] = user['refreshToken']
		
		user = User.objects.get(username = username)
		name = user.first_name
		token = Token.objects.get(user=user)
		return render(request, 'index.html', {"username" : username, "name" : name, "token" : token})
	else:
		return redirect("auth")

def datasetRequestPage(request):
	if request.session.has_key('session_id'):
		try:
			username = settings.FIREBASE_AUTH.get_account_info(request.session['session_id'])['users'][0]['email']
		except requests.exceptions.HTTPError:
			user = settings.FIREBASE_AUTH.refresh(request.session['refreshToken'])
			request.session['session_id'] = user['idToken']
			request.session['refreshToken'] = user['refreshToken']
		
		user = User.objects.get(username = username)
		name = user.first_name

		if request.method == 'POST':
			postData = request.POST
			uid = uuid.uuid1()
			created_by = UserProfile.objects.get(name=name, email=username)
			
			print(postData)
			print(request.POST)
			questionsKeys = [key for key in postData.keys() if "question-" in key]
			data = []
			for question in questionsKeys:
				qData = {}
				qData['question'] = postData[question]
				qData['datatype'] = postData["datatype-" + question[-1]]
				qData['choices'] = postData.getlist(question[-1] + "-options")
				data.append(qData)
			
			dataset = Datasets.objects.create(dataset_name=postData['dataset-name'], description=postData['description'], usecase=postData['usecase'], required_size=postData["required-size"], created_by=created_by, uid=uid, entry_time=timezone.now(), data=json.dumps(data))
			dataset.save()

			return HttpResponse(uid)
		
		return render(request,"dataset-request.html")

	else:
		return redirect("auth")
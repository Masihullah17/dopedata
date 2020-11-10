# Django imports
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse

# Python imports
import os
import requests
import uuid
import json

# Model Imports
from data.models import UserProfile, Datasets

# Google Drive API Imports
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

def authentication(request):
	if request.method == "POST":
		if 'login' in request.POST:
			email=request.POST.get('email')
			passw = request.POST.get("password")
			try:
				user = settings.FIREBASE_AUTH.sign_in_with_email_and_password(email,passw)
				user = settings.FIREBASE_AUTH.refresh(user['refreshToken'])
			except Exception as e:
				print(e)
				message = "Invalid Crediantials!"
				return render(request,"authentication.html", {"errorlogin":message})

			request.session['session_id'] = user['idToken']
			request.session['refreshToken'] = user['refreshToken']

			return redirect('index')
		elif 'signup' in request.POST:
			name = request.POST.get('name')
			email = request.POST.get('email')
			password = request.POST.get("password")
			confirmPassword = request.POST.get("confirm-password")

			if password == confirmPassword:
				try:
					user = settings.FIREBASE_AUTH.create_user_with_email_and_password(email, password)
					user_entry = User.objects.create(first_name=name, username=email)
					user_entry.save()

					profile = UserProfile.objects.create(name=name, email=email, joined=timezone.now())
					profile.save()
					
					access_token = Token.objects.create(user=user_entry)

					return render(request, 'authentication.html', {"message" : "Account created! Login now."})

				except Exception as e:
					return render(request, 'authentication.html', {"signup" : "Yes", "error" : "Weak Password!!"})
			else:
				return render(request, 'authentication.html', {"signup" : "Yes", "error" : "Passwords didn't match!!"})
	return render(request, 'authentication.html')

def logout(request):
	try:
		del request.session['session_id']
	except:
		pass
	return redirect("authentication")

def  login_required(func):
	def checkLogin(request, **kwargs):
		if request.session.has_key('session_id'):
			try:
				username = settings.FIREBASE_AUTH.get_account_info(request.session['session_id'])['users'][0]['email']	
			except requests.exceptions.HTTPError:
				user = settings.FIREBASE_AUTH.refresh(request.session['refreshToken'])
				request.session['session_id'] = user['idToken']
				request.session['refreshToken'] = user['refreshToken']
				username = settings.FIREBASE_AUTH.get_account_info(request.session['session_id'])['users'][0]['email']
			
			request.session['username'] = username
			return func(request, **kwargs)
		else:
			print("Session id not found")
			return redirect("authentication")
	return checkLogin

@login_required
def index(request):
	user = User.objects.get(username = request.session['username'])
	name = user.first_name
	token = Token.objects.get(user=user)
	return render(request, 'index.html', {"username" : request.session['username'], "name" : name, "token" : token})

@login_required
def base(request):
	return render(request, 'base.html')

@login_required
def profile(request):
	user = User.objects.get(username = request.session['username'])
	name = user.first_name

	username = request.session['username']
	userProfile = UserProfile.objects.get(name=name, email=username)
	token = Token.objects.get(user=user)
	context = {}
	context['name'] = name
	context['bio'] = userProfile.bio
	context['badges'] = json.loads(userProfile.badges)
	context['points'] = userProfile.points
	context['level'] = userProfile.level
	context['isPremiumUser'] = userProfile.is_premium_user
	context['joined'] = userProfile.joined
	context['numRequets'] = userProfile.num_requests
	context['numContributions'] = userProfile.num_contributions

	return render(request, 'userprofile.html', context=context)

@login_required
def specificDataset(request, name):
	user = User.objects.get(username = request.session['username'])
	name = user.first_name

	return render(request, 'dataset.html')


@login_required
def dashboard(request):
	user = User.objects.get(username = request.session['username'])
	name = user.first_name

	return render(request, 'dashboard.html')

@login_required
def datasetRequestPage(request):
	user = User.objects.get(username = request.session['username'])
	name = user.first_name

	if request.method == 'POST':
		postData = request.POST
		uid = uuid.uuid1()
		created_by = UserProfile.objects.get(name=name, email=request.session['username'])
		
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
	
	return render(request,"request.html")

def gDriveAPI(request):
	return render(request, 'gdrive.html')

def googleDriveAPI(request):
	pass

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.utils import timezone
import requests as http
import json


def userProfile(request):
	r = http.get(url="http://127.0.0.1:8000/data/api/users/masihulla17@gmail.com/", headers={"Authorization" : "Token 26a263ec3e908a0c26ac37794d0de57054f582e1"})
	details = r.json()

	return render(request, "app/profile.html", context=details)

def search(request):
	dataset = {}
	if request.method == 'POST':
		searchterm = request.POST['search']
		d = http.get(url="http://127.0.0.1:8000/data/api/search/" + searchterm + "/", headers={"Authorization" : "Token 26a263ec3e908a0c26ac37794d0de57054f582e1"})
		dataset = d.json()
		dataset = {'results' : dataset}

	return render(request, "app/search.html", context=dataset)


def contribute(request):
	data = {}
	if request.method == "POST":
		try:
			data = {"data" : json.dumps(json.loads(request.POST['json'])["data"]), "request-id" : request.POST['requestid']}
			r = http.post("http://127.0.0.1:8000/data/api/contribute/", headers={"Authorization" : "Token 26a263ec3e908a0c26ac37794d0de57054f582e1"}, data=data, files=request.FILES)
			data = r.json()

			if "request-id" in data:
				data['requestid'] = data['request-id']
			if "contribution-id" in data:
				data['contributionid'] = data['contribution-id']
		except Exception as e:
			print(e)
			data = {"status" : "Error Occured. Please try again."}
	return render(request, "app/contribute.html", context=data)

def requestpage(request):
	data = {}
	if request.method == "POST":
		try:
			data = json.loads(request.POST['json'])
			r = http.post("http://127.0.0.1:8000/data/api/request/", headers={"Authorization" : "Token 26a263ec3e908a0c26ac37794d0de57054f582e1"}, data=data)
			data = r.json()
			print(data)
			if "request-id" in data:
				data['requestid'] = data['request-id']
		except:
			data = {"status" : "Error Occured. Please try again."}
	return render(request, "app/request.html", context=data)

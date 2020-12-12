from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from data.models import UserProfile
from django.utils import timezone
from django.forms.models import model_to_dict

class TestAPIView(APITestCase):
	def test_anonymous_cannot_access(self):
		response = self.client.get(reverse("request_dataset_post"))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_access(self):
		user = User.objects.create_user("Masihullah," "masihulla17@gmail.com", "abcd1234")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
		response = self.client.get("/data/api/users/masihulla17@gmail.com/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		data = model_to_dict(profile)
		response_data = response.json()
		self.assertEqual(response_data['name'], data['name'])
		self.assertEqual(response_data['email'], data['email'])

	def test_profile_noauth(self):
		response = self.client.get("/data/api/users/userdoesnotexists/")
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_profile(self):
		user = User.objects.create_user("Masihullah," "masihulla17@gmail.com", "abcd1234")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
		response = self.client.get("/data/api/users/userdoesnotexists/")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_search_noauth(self):
		response = self.client.get("/data/api/search/doesnotexists/")
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_search(self):
		user = User.objects.create_user("Masihullah," "masihulla17@gmail.com", "abcd1234")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
		response = self.client.get("/data/api/search/doesnotexists/")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_request_noauth(self):
		response = self.client.get("/data/api/request/")
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_request(self):
		user = User.objects.create_user("Masihullah," "masihulla17@gmail.com", "abcd1234")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
		response = self.client.get("/data/api/request/")
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_contribute_noauth(self):
		response = self.client.get("/data/api/contribute/")
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_contribute(self):
		user = User.objects.create_user("Masihullah," "masihulla17@gmail.com", "abcd1234")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))
		response = self.client.get("/data/api/contribute/")
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
	
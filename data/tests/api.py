from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from data.models import UserProfile
from django.utils import timezone
from django.forms.models import model_to_dict

class TestDownloadView(APITestCase):
	def test_anonymous_cannot_access(self):
		response = self.client.get(reverse("request_dataset_post"))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_see_contacts(self):
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


	
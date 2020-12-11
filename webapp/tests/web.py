from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from data.models import UserProfile
from django.urls import reverse

class TestWeb(TestCase):
	def test_login_form(self):
		data = {
			"login" : 'true',
			"email": "masihulla17@gmail.com",
			"password": "abcd1234",
		}

		user = User.objects.create(username="masihulla17@gmail.com", password="abcd1234", first_name="Masihullah")
		token = Token.objects.create(user=user)
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())

		response = self.client.post(reverse('authentication'), data=data)
		self.assertRedirects(response, reverse('dashboard'))
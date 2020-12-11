from django.test import TestCase
from data.models import *
from django.utils import timezone

from model_bakery import baker

class TestModels(TestCase):
	def test_model_str(self):
		profile = UserProfile.objects.create(name="Masihullah", email="masihulla17@gmail.com", joined=timezone.now())
		dataset = Datasets.objects.create(created_by=profile, dataset_name="Test", uid="1", description="Unit testing the models str", usecase="testing", entry_time=timezone.now(), required_size=10)
		contribution = Contributions.objects.create(contributed_by=profile, contribution_time=timezone.now(), request_uid=1, contribution_uid=1)
		gdrive = GoogleDriveConnections.objects.create(user=profile, is_connected=False)

		self.assertEqual(str(profile), "Masihullah_masihulla17@gmail.com")
		self.assertEqual(str(dataset), "Test_1")
		self.assertEqual(str(contribution), "1")
		self.assertEqual(str(gdrive), "Masihullah False")
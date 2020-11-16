from django.db import models
import json

class UserProfile(models.Model):
	name = models.CharField(max_length=500)
	email = models.EmailField()
	bio = models.TextField(default='', null=True, blank=True)
	profile_pic = models.ImageField(null=True, blank=True)
	joined = models.DateTimeField()
	num_requests = models.IntegerField(default=0)
	num_contributions = models.IntegerField(default=0)
	is_premium_user = models.BooleanField(default=False)
	points = models.IntegerField(default=0)
	badges = models.TextField(default=json.dumps([]))
	level = models.IntegerField(default=0)

	def __str__(self):
		return self.name + "_" + self.email

class Datasets(models.Model):
	created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	dataset_name = models.CharField(max_length=500)
	uid = models.CharField(max_length=50)
	description = models.TextField()
	usecase = models.TextField()
	required_size = models.IntegerField()
	entry_time = models.DateTimeField()
	data = models.TextField(default=json.dumps([]))
	url = models.URLField(default=None, null=True, blank=True)
	is_approved = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	delete_uid = models.CharField(max_length=50, default='', blank=True, null=True)
	stop_accepting_contributions = models.BooleanField(default=False)
	num_filled = models.IntegerField(default=0)

	def __str__(self):
		status = "DELETED_" if self.is_deleted else "NOT-ACCEPTING_" if self.stop_accepting_contributions else ""
		return status + self.dataset_name + "_" + self.uid
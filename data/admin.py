from django.contrib import admin
from data.models import UserProfile, Datasets

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Datasets)
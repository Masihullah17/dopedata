from django.contrib import admin
from data.models import UserProfile, Datasets, Contributions, FilesUploads

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Datasets)
admin.site.register(Contributions)
admin.site.register(FilesUploads)
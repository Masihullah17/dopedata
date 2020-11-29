from django.contrib import admin
from data.models import UserProfile, Datasets, Contributions, FilesUploads, GoogleDriveConnections

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Datasets)
admin.site.register(Contributions)
admin.site.register(FilesUploads)
admin.site.register(GoogleDriveConnections)
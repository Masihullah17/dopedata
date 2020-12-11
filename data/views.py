import csv

from django.shortcuts import render
from django.http import HttpResponse

from .models import Contributions

def export(request):
    response = HttpResponse(content_type='csv')

    writer = csv.writer(response)
    writer.writerow(['time', 'id', 'data', 'verification' ])

    for member in Contributions.objects.filter(deleted=False).values_list('contribution_time', 'contribution_uid', 'data', 'verified'):
        writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="contributions.csv"'

    return response

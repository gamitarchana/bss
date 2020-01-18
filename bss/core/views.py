from django.shortcuts import render
from django.http import JsonResponse
from .models import ServiceArea
import json
# Create your views here.

def service_area(request, city):
    localities = ServiceArea.objects.filter(city=city)
    service_area = []
    for locality in localities:
        print(locality.locality)
        service_area.append({"locality":locality.locality})

    #print(localities)
    #localities = json.loads(localities)
    return JsonResponse({'service_area': service_area})

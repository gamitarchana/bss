from django.shortcuts import render, redirect, get_object_or_404
from bss.core.models import ServiceArea
from .models import Babysitter


# Create your views here.
def job_profile(request):

    '''cities = ServiceArea.objects.values('city').distinct()

    context = {
        'cities': cities,
    }'''
    if request.method == 'POST':
        hours_per_day = request.POST.get('hoursperday')
        no_of_children = request.POST.get('numberofchildren')
        location1 = get_object_or_404(ServiceArea, id=request.POST.get('location1'))
        location2 = get_object_or_404(ServiceArea, id=request.POST.get('location2'))
        location3 = get_object_or_404(ServiceArea, id=request.POST.get('location3'))
        babysitter = get_object_or_404(Babysitter, user_id=request.user.id)
        #print(hours_per_day)
        #print(no_of_children)
        #print(location1)
        #print(location2)
        #print(location3)
        babysitter = get_object_or_404(Babysitter, user_id=request.user.id)
        if babysitter:
            #job_preference = JobPreference.objects.create(
            #    hours_per_day = hours_per_day,
            #    no_of_children = no_of_children,
            #    )
            #job_preference.locations.add(location1)
            #job_preference.locations.add(location2)
            #job_preference.locations.add(location3)
            babysitter.peference_hours_per_day = hours_per_day
            babysitter.preference_no_of_children = no_of_children
            babysitter.preference_locations.add(location1)
            babysitter.preference_locations.add(location2)
            babysitter.preference_locations.add(location3)
            babysitter.save()



        #JobPreference.objects.create(content_object=location1)
        '''service_request = ServiceRequest.objects.create(
            location = location,
            client = client,
            service_package = service_package,
        )
        '''
        return redirect('/')
    service_areas = ServiceArea.objects.all()

    context = {
        'service_areas': service_areas,
    }
    return render (request, 'user/job_profile.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, ServiceRequest, SpeficServiceCharge, Shift, ShiftTimeSlot, BasicServicePackage
from bss.core.models import ServiceArea
from django.contrib.auth.decorators import login_required

def service_packages_view(request):
    #next = '/'
    #form = LoginForm(request.POST or None)
    '''if form.is_valid():
        username = form.cleaned_data.get('username')
        #email = form.cleaned_date.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        #if next:
            #return redirect(next)
        return redirect('/')
    context ={
        'form': form,

    }'''
    if request.method == 'POST':
        #service_package = get_object_or_404(ServicePackage, id=request.POST.get('service_package'))
        #location = request.POST.get('location')
        #client = get_object_or_404(Client, user_id=request.user.id)
        request.session['service'] = request.POST.get('service')
        request.session['location'] = request.POST.get('location')
        '''service_request = ServiceRequest.objects.create(
            location = location,
            client = client,
            service_package = service_package,
        )
        '''
        return redirect('/service_request/')
    services = Service.objects.all()
    service_areas = ServiceArea.objects.all()
    context ={
        'services': services,
        'service_areas': service_areas,

    }
    return render (request, 'services/service_packages.html', context)


@login_required(login_url='/login/?next=/service_request/')
def service_request_view(request):
    specific_service = None
    shift = None
    working_hours = None
    if request.method == 'POST':
        if request.session['page_num'] == 1:
            request.session['page_num'] = 2
            specific_service = request.POST.get('specific_service')#request.session['specific_service']
            shift=request.POST.get('shift')#request.session['shift']
            time_slots = ShiftTimeSlot.objects.filter(shift__type=shift)
            request.session['specific_service'] = specific_service
            request.session['shift'] = shift
            print("Shift.DAY")
            print(shift)
            print(Shift.DAY)
            print(type(shift))
            print(type(Shift.DAY))
            if shift == str(Shift.DAY):
                working_hours = Shift.HOURS_CHOICES
                print("------working_hours")
                print(working_hours)
                context ={
                    'working_hours' : working_hours,
                    }
                return render (request, 'services/service_request_2.html', context)
            else:
                request.session['page_num'] = 3
                #working_hours = request.POST.get('hours')
                shift = request.session['shift']
                print("else -------------shift-----working_hours")
                #print(working_hours)
                #print(shift)
                time_slots = ShiftTimeSlot.objects.filter(shift__type=shift)
                context ={
                    'time_slots' : time_slots,
                }
                return render (request, 'services/service_request_3.html', context)

        elif request.session['page_num'] == 2:
            request.session['page_num'] = 3
            #working_hours = request.POST.get('hours')
            shift = request.session['shift']
            time_slots = None
            if shift == str(Shift.DAY):
                working_hours = request.POST.get('hours')
                request.session['hours_per_day'] = working_hours
                time_slots = ShiftTimeSlot.objects.filter(shift__type=shift, shift__hours_per_day=working_hours)
            else:
                time_slots = ShiftTimeSlot.objects.filter(shift__type=shift)
            #print("shift-----working_hours")
            #print(working_hours)
            #print(shift)
            time_slots = ShiftTimeSlot.objects.filter(shift__type=shift, shift__hours_per_day=working_hours)
            context ={
                'time_slots' : time_slots,
            }
            return render (request, 'services/service_request_3.html', context)
            '''client = get_object_or_404(Client, user_id=request.user.id)
            location = get_object_or_404(ServiceArea, id=request.POST.get('location'))
            service_request = ServiceRequest.objects.create(
                location = location,
                client = client,
                service_package = service_package,
            )'''
            #Child.objects.create(first_name=first_name1, last_name=last_name1, gender=gender1, date_of_birth=date_of_birth1, service_request=service_request)
    #        first_name2 = request.POST.get('firstname2')
    #        last_name2 = request.POST.get('lastname2')
    #        gender2 = request.POST.get('gender2')
            #date_of_birth2 = request.POST.get('dateofbirth2')
            #if first_name2 and last_name2 and gender2 and date_of_birth2:
            #    Child.objects.create(first_name=first_name2, last_name=last_name2, gender=gender2, date_of_birth=date_of_birth2, service_request=service_request)
            ''''babysitters = Babysitter.objects.filter(user__user_type=UserProfile.BABYSITTER, peference_hours_per_day = service_package.hours_per_day, preference_no_of_children = service_package.no_of_children)
            print(babysitters)
            recommended_babysitters = Babysitter.objects.filter(id__in=Subquery(babysitters.values('id')), preference_locations=location)
            print(recommended_babysitters)
            for recommeded in recommended_babysitters:
                service_request.babysitter_recommendations.add(recommeded)
                recommeded.status = BabysitterRecommendation.RECOMMENDED
                recommeded.save()
            return redirect('/')'''
        elif request.session['page_num'] == 3:
            request.session['page_num'] = 4
            sp=request.session['service']
            service = get_object_or_404(Service, id=request.session['service'])
            specific_service = request.session['specific_service']
            shift=request.session['shift']
            time_slot = request.POST.get('time_slot')
            hours_per_day_id = None
            hours_per_day = None
            night_charges_package = None
            night_charges = 0
            total_charges = 0
            if int(shift) == Shift.NIGHT:
                hours_per_day = 12
                night_charges_package = get_object_or_404(SpeficServiceCharge, type = SpeficServiceCharge.NIGHT)
                night_charges = night_charges_package.additionl_charges
                total_charges = total_charges+night_charges
            else:
                hours_per_day_id = request.session['hours_per_day']

            #print(type(hours_per_day_id))
            if hours_per_day_id:
                for hours in Shift.HOURS_CHOICES:
                    print(hours)
                    print(type(hours[0]))
                    if hours[0]==int(hours_per_day_id):
                        print(hours[1])
                        hours_per_day = int(hours[1])
            #basic_package = BasicServicePackage.objects.filter(service=service, hours_per_day=hours_per_day)

            basic_package = get_object_or_404(BasicServicePackage, service_id=service.id, hours_per_day=hours_per_day)
            specific_service_charges = get_object_or_404(SpeficServiceCharge, id=specific_service)
            total_charges = total_charges+basic_package.charges+specific_service_charges.additionl_charges
            print("---charges---")
            print(specific_service)
            print(shift)
            print(time_slot)
            print(hours_per_day)
            print(basic_package.charges)
            print(specific_service_charges.additionl_charges)
            print(specific_service_charges.name)
            if night_charges_package:
                print(night_charges_package.additionl_charges)
            context = {
                'basic_charges':basic_package.charges,
                'specific_charges':specific_service_charges.additionl_charges,
                'night_charges':night_charges,
                'specific_service':specific_service_charges.name,
                'total_charges':total_charges,
            }
            return render (request, 'services/service_request_4.html', context)
        elif request.session['page_num'] == 4:
            print("--------------final page-------------")
            return render (request, 'services/service_request_5.html')
    #service_areas = ServiceArea.objects.all()
    #page_num=1
    #page_num
    location = request.session['location']
    sp=request.session['service']
    service = get_object_or_404(Service, id=request.session['service'])
    #hours = Shift.HOURS_CHOICES[0]
    '''for hours in Shift.HOURS_CHOICES:
        print(hours)
        print(hours[1])
        if(hours[0]==1):
            print(hours[1])'''
    #print(hours)
    #print("sp")
    #print(sp)
    #location = get_object_or_404(ServiceArea, id=request.POST.get('location'))
    '''service_request = ServiceRequest.objects.create(
        location = location,
        client = client,
        service_package = service_package,
    )'''
    #basic_service = BasicServicePackage.objects.filter(service=service)
    specific_services = SpeficServiceCharge.objects.filter(service=service, type=SpeficServiceCharge.NORMAL)
    shifts = Shift.SHIFT_TYPE_CHOICES
    #shift.append(Shift.DAY)
    #shift.append(Shift.NIGHT)
    request.session['page_num'] = 1
    context ={
        #'service_areas': service_areas,
        'specific_services' : specific_services,
        'shifts':shifts,
        'service' : service,
    }
    return render (request, 'services/service_request.html', context)

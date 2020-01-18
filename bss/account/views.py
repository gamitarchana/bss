from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.views import PasswordResetView

from .forms import LoginForm, UserSignUpForm
from bss.user.models import UserProfile, Babysitter
#from bss.babysitter.models import JobRequest
from .forms import UserPasswordResetForm

def login_user(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        #email = form.cleaned_date.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/service_packages/')
    context ={
        'form': form,
    }
    return render (request, 'account/login.html', context)

def signup_user(request):
    #next = '/'
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        #email = form.cleaned_date.get('email')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        is_jobseeker = request.POST.get('is_jobseeker')
        print("--jobseeker--")
        print(is_jobseeker)
        if not is_jobseeker:
            user.user_type = UserProfile.CLIENT
            print("UserProfile.CLIENT")
            print(user.user_type)
        else:
            user.user_type = UserProfile.JOBSEEKER
            print("UserProfile.JOBSEEKER")
            print(user.user_type)
        user.save()
        print(user.user_type)
        print("iiiii")
        print(UserProfile.JOBSEEKER)
        '''if user.user_type == UserProfile.JOBSEEKER:
            print("jobseeker------------------")
            babysitter = Babysitter.objects.get_or_create(user = user)
            print(babysitter.id)
            JobRequest.objects.get_or_create(babysitter_id = babysitter.id)'''
        #Client.objects.get_or_create(user = instance)
        user = authenticate(username=user.username, password=password)
        login(request, user)
        if user.user_type == UserProfile.CLIENT:
            return redirect('/service_packages/')
        elif user.user_type == UserProfile.JOBSEEKER:
            return redirect('/job_profile/')
        return redirect('/')
    context ={
        'form': form,

    }
    return render (request, 'account/signup.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')

class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm

"""bss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from adminplus.sites import AdminSitePlus

from bss.home import views as views_home
from bss.account import views as views_account
from bss.user import views as views_user
from bss.services import views as views_services
from bss.core import views as views_core
from django.contrib.auth import views as auth_views

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_home.home),
    path('login/', views_account.login_user, name='login'),
    path('signup/', views_account.signup_user),
    path('logout/', views_account.logout_user),

    path('password_change/', views_account.UserPasswordResetView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('service_packages/', views_services.ServiceRequestFormWizard.as_view(), name='service_packages'),
    path('service_packages/', views_services.service_packages_view, name='service_packages'),
    path('service_request/', views_services.service_request_view, name='service_request'),
    path('job_profile/', views_user.job_profile, name='job_profile'),
    path('job_profile/', views_user.job_profile, name='job_profile'),
    path('service_area/<str:city>', views_core.service_area, name='service_area'),


]

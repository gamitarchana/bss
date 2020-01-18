from django import forms
from .models import ServiceRequest, ServicePackage


class ServiceRequestFormStepOne(forms.Form):
    location = forms.CharField(max_length=255)
    service_package = forms.ModelMultipleChoiceField(queryset=ServicePackage.objects.all())

    '''class Meta:
        model = ServiceRequest
        fields = [
            'client',
            'service_package',
            'location',
        ]'''

class ServicesRequestFormStepTwo(forms.Form):
    location = forms.CharField(max_length=255)
    '''class Meta:
        model = ServiceRequest
        fields = [
            'location',
        ]'''

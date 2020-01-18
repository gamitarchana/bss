from django.contrib import admin
from .models import ServiceArea

# Register your models here.

class ServiceAreaAdmin(admin.ModelAdmin):
    fields = ['locality', 'city']
admin.site.register(ServiceArea, ServiceAreaAdmin)

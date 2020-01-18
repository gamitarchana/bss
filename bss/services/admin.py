from django.contrib import admin
from .models import Service, BasicServicePackage, SpeficServiceCharge, Shift, ShiftTimeSlot, ServiceRequest
from django_reverse_admin import ReverseModelAdmin


class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)



class BasicServicePackageAdmin(admin.ModelAdmin):
    pass
admin.site.register(BasicServicePackage, BasicServicePackageAdmin)



class SpeficServiceChargeAdmin(admin.ModelAdmin):
    pass
admin.site.register(SpeficServiceCharge, SpeficServiceChargeAdmin)

class ShiftInline(admin.StackedInline):
    model = Shift
    verbose_name = "Shift"
    verbose_name_plural = "Shifts"
    fields = ["type", "hours_per_day"]
    readonly_fields = ("type", "hours_per_day")
    max_num=1


'''class ShiftTimeSlotAdmin(admin.ModelAdmin):
    #fields = ['client', 'service_package', 'location']
    #readonly_fields = ['client', 'service_package', 'location']
    inlines = [ShiftInline]
admin.site.register(ShiftTimeSlot, ShiftTimeSlotAdmin)'''

class ShiftTimeSlotAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = ['start_time', 'end_time',('shift', {'fields': ['type', 'hours_per_day']}),]
admin.site.register(ShiftTimeSlot, ShiftTimeSlotAdmin)



'''class ServicePackageAdmin(admin.ModelAdmin):
    pass
admin.site.register(ServicePackage, ServicePackageAdmin)

from django.forms import BaseInlineFormSet

class ChildInline(admin.StackedInline):
    model = Child
    verbose_name = "Child"
    verbose_name_plural = "Children"
    fields = ["first_name", "last_name", "gender", "date_of_birth"]
    readonly_fields = ("first_name", "last_name", "gender", "date_of_birth")
    max_num=2'''

def make_pending_wallet_recharge(modeladmin, request, queryset):
    queryset.update(status=ServiceRequest.WALLET_RECHARGE_PENDING)
make_pending_wallet_recharge.short_description = "Wallet Recharge Pending"

def make_request_meeting_reschedule(modeladmin, request, queryset):
    queryset.update(status=ServiceRequest.MEETING_RESCHEDULE_REQUEST)
make_request_meeting_reschedule.short_description = "Request a reschedule for the the meeting"

def make_payment_due(modeladmin, request, queryset):
    queryset.update(status=ServiceRequest.PAYMENT_DUE)
make_payment_due.short_description = "Payment due"

class BabysitterRecommendationInline(admin.TabularInline):
    model = ServiceRequest.babysitter_recommendations.through
    extra = 3

class ServiceRequestAdmin(admin.ModelAdmin):
    fields = ['client', 'basic_service_package', 'extra_service_package','location','shift_time_slot']
    #readonly_fields = ['client', 'service_package', 'location']
    inlines = [BabysitterRecommendationInline]
    actions = [make_pending_wallet_recharge, make_request_meeting_reschedule, make_payment_due]

    #print("ServiceRequestAdmin inlines")
    #print(inlines)
admin.site.register(ServiceRequest, ServiceRequestAdmin)




'''class ServiceRequestAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [
    ('service_package',{'fields': ['name']}),
                      ]
admin.site.register(ServiceRequest, ServiceRequestAdmin)'''

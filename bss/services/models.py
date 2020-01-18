from django.db import models
#from bss.core.models import StateableObject
from bss.user.models import Client, Babysitter
from django.db.models import Max
from bss.core.models import ServiceArea
# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    icon = models.ImageField(upload_to='service_icons', null=True, blank=True)

    def __str__(self):
        return self.name

class BaseServicePackage(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    charges = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    class Meta:
        abstract = True

class BasicServicePackage(models.Model):
    #service_id = models.CharField(unique=True, editable=False, max_length=10)
    #service = models.OneToOneField(Service, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='basic_service_package')
    name = models.CharField(max_length=150, null=False, blank=False)
    hours_per_day = models.PositiveSmallIntegerField(null=True, blank=True)
    duration_in_days = models.PositiveSmallIntegerField(null=True, blank=True)
    #no_of_children = models.PositiveSmallIntegerField(null=False, blank=False)
    charges = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name

    '''def save(self, **kwargs):
        if not self.service_id:
            max = ServicePackage.objects.aggregate(service_id_max=Max('service_id'))['service_id_max']
            print("------max----")
            print(max)
            if max:
                max = max[3:]
                max = int(max)+1
                print(max)
                print("------max end----")
            else:
                max = 1
            max=str(max).rjust(5, '0')
            self.service_id = "{}{}".format('SP', max )
        super().save(*kwargs)'''

class SpeficServiceCharge(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    #service = models.OneToOneField(Service, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='extra_service_package')
    duration_in_days = models.PositiveSmallIntegerField(null=False, blank=False)
    additionl_charges = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    NORMAL = 1
    NIGHT = 2
    TRAVEL = 3

    SERVIES_TYPES_CHOICES = (
        (NORMAL, 'Normal'),
        (NIGHT, 'Night'),
        (TRAVEL, 'Travel'),
        )
    type = models.PositiveSmallIntegerField(choices=SERVIES_TYPES_CHOICES, default = NORMAL)

    def __str__(self):
        return self.name

class Shift(models.Model):
    DAY = 1
    NIGHT = 2

    SHIFT_TYPE_CHOICES = (
        (DAY, 'Day'),
        (NIGHT, 'Night'),
        )
    type = models.PositiveSmallIntegerField(choices=SHIFT_TYPE_CHOICES, default = DAY)
    EIGHT = 1
    TEN = 2
    TWELVE = 3

    HOURS_CHOICES = (
        (EIGHT, 8),
        (TEN, 10),
        (TWELVE, 12),
        )
    type = models.PositiveSmallIntegerField(choices=SHIFT_TYPE_CHOICES, default = DAY)
    hours_per_day = models.PositiveSmallIntegerField(choices=HOURS_CHOICES, default = EIGHT)

    #def __str__(self):
    #    return self.type + " - " +self.hours_per_day +"hrs"

class ShiftTimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='time_slots')

    def __str__(self):#str(self.shift.type.value) + " - "+
        return  str(self.start_time) +  " - "  + str(self.end_time)

class ServiceRequest(models.Model):
    #status = models.PositiveSmallIntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='service_requests')
    basic_service_package = models.ForeignKey(BasicServicePackage, on_delete=models.CASCADE, related_name='service_requests')
    additional_service_charges = models.ForeignKey(SpeficServiceCharge, on_delete=models.CASCADE, related_name='service_requests')
    location = models.ForeignKey(ServiceArea, null=False, on_delete = models.CASCADE, related_name='service_requests')
    shift_time_slot = models.ForeignKey(ShiftTimeSlot, null=False, on_delete = models.CASCADE, related_name='service_requests')
    NEW = 1
    NEW_PROFILE = 2
    PROFILE_ACCEPTED = 3
    PROFILE_REJECTED = 4
    MEETING_SCHEDULED = 5
    MEETING_RESCHEDULE_REQUEST = 6
    MEETING_ACCEPTED = 7
    MEETING_DONE = 8
    WALLET_RECHARGE_PENDING = 9
    WALLET_RECHARGED = 10
    TRIAL = 11
    ACCEPTED = 12
    REJECTED = 13
    PAYMENT_DUE = 14

    STATUS_CHOICES = (
        (NEW, 'new'),
        (NEW_PROFILE, 'new profile'),
        (PROFILE_ACCEPTED, 'profile accepted'),
        (PROFILE_REJECTED, 'profile rejected'),
        (MEETING_SCHEDULED, 'meeting scheduled'),
        (MEETING_RESCHEDULE_REQUEST, 'meeting reschedule request'),
        (MEETING_ACCEPTED, 'meeting accepted'),
        (MEETING_DONE, 'meeting done'),
        (WALLET_RECHARGE_PENDING, 'wallet recharge pending'),
        (WALLET_RECHARGED, 'wallet recharged'),
        (TRIAL, 'trail'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (PAYMENT_DUE, 'payment due'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default = NEW)
    babysitter_recommendations = models.ManyToManyField(Babysitter, through='BabysitterRecommendation')
    #comments =
    '''def __init__(self,  *args, **kwargs):
        super(ServiceRequest, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('status')[0]._choices = STATUS_CHOICES
        self._meta.get_field_by_name('status')[0]._default = NEW'''

class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    FEMALE = 1
    MALE = 2
    GENDER_CHOICES = (
        (FEMALE, 'female'),
        (MALE, 'male'),
    )

    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default = FEMALE)

    #client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name='children')
    service_request = models.ForeignKey(ServiceRequest, on_delete = models.CASCADE, related_name = 'children')

class BabysitterRecommendation(models.Model):
    babysitter = models.ForeignKey(Babysitter, on_delete = models.CASCADE, related_name = 'recommendations')
    service_request = models.ForeignKey(ServiceRequest, on_delete = models.CASCADE, related_name = 'recommendations')
    AVAILABLE = 1
    RECOMMENDED = 2
    ACTIVE = 3
    REJECTED = 4
    STATUS_CHOICES = (
        (AVAILABLE, 'available'),
        (RECOMMENDED, 'recommended'),
        (ACTIVE, 'active'),
        (REJECTED, 'rejected'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default = AVAILABLE)

    '''def __init__(self,  *args, **kwargs):
        super(Recommendation, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('status')[0]._choices = STATUS_CHOICES
        self._meta.get_field_by_name('status')[0]._default = AVAILABLE'''

    #comment =  models.CharField(max_length=255)
    #comment_published_date = models.DateTimeField(auto_now_add = True)

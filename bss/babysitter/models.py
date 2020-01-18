from django.db import models
#from bss.user.models import Babysitter
#from django.dispatch import receiver
#from bss.core.models import ServiceArea
#from bss.user.models import UserProfile

'''class JobPreference(models.Model):
    hours_per_day = models.PositiveSmallIntegerField(null=False, blank=False)
    #duration_in_days = models.PositiveSmallIntegerField(null=False, blank=False)
    no_of_children = models.PositiveSmallIntegerField(null=False, blank=False)

    locations = models.ManyToManyField(ServiceArea)

class Babysitter(models.Model):
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    job_preference = models.OneToOneField(JobPreference, null=True, on_delete = models.CASCADE)
    #is_jobseeker = models.BooleanField(_('jobseeker'), default=True)

    def __str__(self):
        return self.user.username

@receiver(post_delete, sender=Babysitter)
def delete_babysitter(sender, instance, using, **kwargs):
    instance.user.delete()

@receiver(post_save, sender=Babysitter)
def create_babysitter(sender, instance, created, **kwargs):
    if instance.user.user_type != UserProfile.JOBSEEKER:
        instance.user.user_type = UserProfile.JOBSEEKER
    JobRequest.objects.get_or_create(babysitter = instance)



class JobRequest(models.Model):
    babysitter = models.OneToOneField(Babysitter, on_delete = models.CASCADE)
    NEW = 1
    PENDING_APPROVAL_FROM_EXECUTIVE = 2
    PENDING_APPROVAL_FROM_ADMIN = 3
    ACCEPTED = 4
    REJECTED = 5
    STATUS_CHOICES = (
        (NEW, 'new'),
        (PENDING_APPROVAL_FROM_EXECUTIVE, 'pending approval from executive'),
        (PENDING_APPROVAL_FROM_ADMIN, 'pending approval from admin'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default = NEW)


'''

# Create your models here.
'''class JobRequest(models.Model):
    babysitter = models.OneToOneField(Babysitter, on_delete = models.CASCADE)
    NEW = 1
    PENDING_APPROVAL_FROM_EXECUTIVE = 2
    PENDING_APPROVAL_FROM_ADMIN = 3
    ACCEPTED = 4
    REJECTED = 5
    STATUS_CHOICES = (
        (NEW, 'new'),
        (PENDING_APPROVAL_FROM_EXECUTIVE, 'pending approval from executive'),
        (PENDING_APPROVAL_FROM_ADMIN, 'pending approval from admin'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default = NEW)


class JobPreference(models.Model):
    hours_per_day = models.PositiveSmallIntegerField(null=False, blank=False)
    duration_in_days = models.PositiveSmallIntegerField(null=False, blank=False)
    no_of_children = models.PositiveSmallIntegerField(null=False, blank=False)
'''

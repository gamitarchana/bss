from django.db import models

from django.contrib.auth.models import PermissionsMixin
#from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
#from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Max
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from bss.core.models import ServiceArea
#from bss.babysitter.models import Babysitter
#from .managers import UserManager

class UserProfile(AbstractUser):
    #id = models.CharField(primary_key=True, editable=False, max_length=10)
    primary_contact_number = PhoneNumberField(null=True, blank=True)
    alternate_contact_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    EMPLOYEE = 1
    BABYSITTER = 2
    CLIENT = 3
    JOBSEEKER = 4
    USER_TYPE_CHOICES = (
        (EMPLOYEE, 'employee'),
        (BABYSITTER, 'babysitter'),
        (CLIENT, 'client'),
        (JOBSEEKER, 'jobseeker'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default = EMPLOYEE)

    '''def save(self, *args, **kwargs):
        if not self.id:
            max = UserProfile.objects.aggregate(id_max=Max('id'))['id_max']
            print(max)
            self.id = "{}{:05d}".format('A', max if max is not None else 1)
        #super().save(*kwargs)
        super(UserProfile, self).save(*args, **kwargs)'''
    '''def save(self, **kwargs):
        if not self.id:
            max = UserProfile.objects.aggregate(id_max=Max('id'))['id_max']
            if max:
                max = max[2:]
                print(max)
                max = int(max)+1
                max=str(max).rjust(5, '0')
            self.id = "{}{}".format('A', max if max is not None else 1)
        super().save(*kwargs)'''

'''class JobPreference(models.Model):
    hours_per_day = models.PositiveSmallIntegerField(null=False, blank=False)
    #duration_in_days = models.PositiveSmallIntegerField(null=False, blank=False)
    no_of_children = models.PositiveSmallIntegerField(null=False, blank=False)

    locations = models.ManyToManyField(ServiceArea)'''

class Employee(models.Model):
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Babysitter(models.Model):
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    #job_preference = models.OneToOneField(JobPreference, null=True, on_delete = models.CASCADE)
    #is_jobseeker = models.BooleanField(_('jobseeker'), default=True)
    working_hours = models.PositiveSmallIntegerField(null=True, blank=False)
    #duration_in_days = models.PositiveSmallIntegerField(null=False, blank=False)
    children_option = models.PositiveSmallIntegerField(null=True, blank=False)
    #service = models.PositiveSmallIntegerField(null=True, blank=False)
    location_preferences = models.ManyToManyField(ServiceArea)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(UserProfile, on_delete = models.CASCADE)
    wallet = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    blocked_babysitters = models.ManyToManyField(Babysitter, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_delete, sender=Employee)
def delete_employee(sender, instance, using, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Babysitter)
def delete_babysitter(sender, instance, using, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Client)
def delete_client(sender, instance, using, **kwargs):
    instance.user.delete()

@receiver(post_save, sender=Babysitter)
def create_babysitter(sender, instance, created, **kwargs):
    if instance.user.user_type != UserProfile.JOBSEEKER:
        instance.user.user_type = UserProfile.JOBSEEKER
    JobRequest.objects.get_or_create(babysitter = instance)


@receiver(post_save, sender=Client)
def create_client(sender, instance, created, **kwargs):
    print('Client post_save create')
    if instance.user.user_type != UserProfile.CLIENT:
        instance.user.user_type = UserProfile.CLIENT

@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):
    print('UserProfile post_save create')
    #print(created)
    #print(instance.user_type)

    if instance.user_type == UserProfile.BABYSITTER or instance.user_type == UserProfile.JOBSEEKER:
        Babysitter.objects.get_or_create(user = instance)
    elif instance.user_type == UserProfile.CLIENT:
        Client.objects.get_or_create(user = instance)
    else:
        #print("employee")
        Employee.objects.get_or_create(user_id = instance.id)

    if not instance.password:
        print('password not set')
        '''reset_form = PasswordResetForm({'email': obj.email})
        assert reset_form.is_valid()
        reset_form.save(
            request=request,
            use_https=request.is_secure(),
            subject_template_name='registration/account_creation_subject.txt',
            email_template_name='registration/account_creation_email.html',
        )'''



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

    def view_user(self, obj):
        return self.user


'''@receiver(post_save, sender=UserProfile)
def save_user_profile(sender, instance, **kwargs):
    print('_-----')
    print('UserProfile post_save save')
    if instance.user_type == instance.CLIENT:
        instance.client.save()
    elif instance.user_type == instance.BABYSITTER:
        instance.babysitter.save()
    else:
        instance.employee.save()'''



'''class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone_number = PhoneNumberField()
    address = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
'''

class Document(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='documents')

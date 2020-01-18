from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#from bss.user.models import UserProfile
#from bss.services.models import ServiceRequest

'''class Document(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='documents')
'''
'''class StateableMixin(models.Model):
    class Meta:
        abstract=True

    status = models.PositiveSmallIntegerField()

'''

#class StateableObject(models.Model):
    #status = models.PositiveSmallIntegerField()
#    pass

class Comment(models.Model):
    content =  models.CharField(max_length=255)
    published_date = models.DateTimeField(auto_now_add = True)
    #user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    #service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='comments')
    #stateable_object = models.ForeignKey(StateableObject, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class ServiceArea(models.Model):
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    '''content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')'''

    def __str__(self):
        return self.locality +', '+ self.city

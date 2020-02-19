from __future__ import unicode_literals
from datetime import timedelta
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from model_utils import Choices
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from ledger.accounts.models import Organisation, Address as LedgerAddress, OrganisationAddress
from ledger.accounts.models import EmailUser


ASSIGNMENT_GROUP = (
   (0, 'taskgroup'),
   (1, 'emailuser'),
   (2, 'emailuser_id'),
)

@python_2_unicode_compatible
class System(models.Model):
    system_id = models.CharField(max_length=10)
    system_name = models.CharField(max_length=256)
    api_key = models.CharField(max_length=256) 
    enabled = models.BooleanField(default=True) 

@python_2_unicode_compatible
class Task(models.Model):
    TASK_TYPE = (
          (0,'Task'),
          (1,'System Task')
    )
    TASK_STATUS = (
          (0,'Closed'),
          (1,'Open')
    )

    task_title = models.CharField(max_length=256)
    task_description = models.TextField(blank=True, null=True, default="") 
    system_reference_number = models.CharField(max_length=256)
    system = models.ForeignKey(System, blank=True, null=True) 
    task_type = models.IntegerField(choices=TASK_TYPE,default=-1)
    #owner_role =
    #assignment_role =
    #esculation =
    status = models.IntegerField(choices=TASK_STATUS,default=1)
    assigned_to = models.ForeignKey(EmailUser, blank=True, null=True)
    deferred_to = models.DateTimeField(null=True, blank=True)
    extra_meta = JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.task_title)

#@python_2_unicode_compatible
#class TaskAttachment(models.Model):

@python_2_unicode_compatible
class TaskGroup(models.Model):
    group_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskGroupAccess(models.Model):
    task_group = models.ForeignKey(TaskGroup, blank=False, null=False)
    user = models.ForeignKey(EmailUser, blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskOwner(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False) 
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1)
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False)
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1)
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskEscalation(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False)
    esculation_dt = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskEscalationAssignment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False)
    esculation = models.ForeignKey(TaskEscalation, blank=False, null=False)
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1) 
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

@python_2_unicode_compatible
class TaskLog(models.Model):

    LOG_ACTION = (
       (0, 'Create'),
       (1, 'Update'),
       (2, 'API Create'),
       (3, 'API Update'),
       (4, 'Assign'),
       (5, 'API Assign')
    )

    task = models.ForeignKey(Task, blank=False, null=False)
    user = models.ForeignKey(EmailUser, blank=True, null=True)
    system = models.ForeignKey(System, blank=True, null=True) 
    action = models.IntegerField(choices=LOG_ACTION, default=1) 
    parameters = JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)



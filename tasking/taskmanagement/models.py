from __future__ import unicode_literals
from datetime import timedelta
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from model_utils import Choices
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from datetime import datetime

today = datetime.now()
today_path = today.strftime("%Y/%m/%d/%H")
private_storage = FileSystemStorage(location=settings.BASE_DIR+"/private-media/task_attachments/"+today_path)

ASSIGNMENT_GROUP = (
   (0, 'taskgroup'),
   (1, 'emailuser'),
   (2, 'ledgergroup'),
)

#@python_2_unicode_compatible
class System(models.Model):
    system_id = models.CharField(max_length=10)
    system_name = models.CharField(max_length=256)
    api_key = models.CharField(max_length=256) 
    enabled = models.BooleanField(default=True) 

#@python_2_unicode_compatible
class Task(models.Model):
    TASK_TYPE = (
          (0,'Task'),
          (1,'System Task')
    )
    TASK_STATUS = (
          (0,'Closed'),
          (1,'Open')
    )
    TASK_PRIORITY = (
          (1, 'Low'), 
          (2, 'Medium'),
          (3, 'High'),
          (4, 'Critical')
    )

    task_title = models.CharField(max_length=256)
    task_description = models.TextField(blank=True, null=True, default="") 
    system_reference_number = models.CharField(max_length=256)
    system = models.ForeignKey(System, blank=True, null=True, on_delete=models.CASCADE,) 
    task_type = models.IntegerField(choices=TASK_TYPE,default=-1)
    task_priority = models.IntegerField(choices=TASK_PRIORITY,default=1) 
    #owner_role =
    #assignment_role =
    #esculation =
    status = models.IntegerField(choices=TASK_STATUS,default=1)
    assigned_to = models.IntegerField(blank=True, null=True)
    deferred_to = models.DateTimeField(null=True, blank=True)
    extra_meta = JSONField(null=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.task_title)

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    filename = models.CharField(max_length=256, default='')
    extension = models.CharField(max_length=50, default='')
    upload = models.FileField(storage=private_storage, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.upload:
            return '{}'.format(self.upload.path)
        else:
            return ''

class TaskComment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    task_comment = models.TextField(blank=True, null=True, default="")
    created_by = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.task_comment)

class TaskCommentAttachment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    task_comment = models.ForeignKey(TaskComment, blank=False, null=False, on_delete=models.CASCADE)
    filename = models.CharField(max_length=256, default='')
    extension = models.CharField(max_length=50, default='')
    upload = models.FileField(storage=private_storage, default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.upload:
            return '{}'.format(self.upload.path)
        else:
            return ''

class GroupCounter(models.Model):
    group_type = models.IntegerField(blank=True, null=True) 
    group_id = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(str(self.total))

#@python_2_unicode_compatible
#class TaskAttachment(models.Model):

#@python_2_unicode_compatible
class TaskGroup(models.Model):
    group_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.group_name


#@python_2_unicode_compatible
class TaskGroupAccess(models.Model):
    task_group = models.ForeignKey(TaskGroup, blank=False, null=False, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#@python_2_unicode_compatible
class TaskOwner(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE) 
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1)
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#@python_2_unicode_compatible
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1)
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#@python_2_unicode_compatible
class TaskEscalation(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    esculation_dt = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#@python_2_unicode_compatible
class TaskEscalationAssignment(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
    esculation = models.ForeignKey(TaskEscalation, blank=False, null=False, on_delete=models.CASCADE,)
    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1) 
    assignment_value = models.IntegerField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#@python_2_unicode_compatible
class TaskLog(models.Model):

    LOG_ACTION = (
       (0, 'Create'),
       (1, 'Update'),
       (2, 'API Create'),
       (3, 'API Update'),
       (4, 'Assign'),
       (5, 'API Assign')
    )

    task = models.ForeignKey(Task, blank=False, null=False,  on_delete=models.CASCADE)
    user = models.IntegerField(blank=True, null=True)
    system = models.ForeignKey(System, blank=True, null=True, on_delete=models.CASCADE) 
    action = models.IntegerField(choices=LOG_ACTION, default=1) 
    parameters = JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)



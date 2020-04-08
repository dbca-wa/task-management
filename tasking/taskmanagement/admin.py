from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.db.models import Q

#from ledger.accounts import admin as ledger_admin
#from ledger.accounts.models import EmailUser
from copy import deepcopy

from taskmanagement import models


class TaskOwnerAdminInline(admin.TabularInline):
    model = models.TaskOwner
    #raw_id_fields = ('user',)
    extra = 0

class TaskAssignmentAdminInline(admin.TabularInline):
    model = models.TaskAssignment
    #raw_id_fields = ('user',)
    extra = 0



@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title','system_reference_number','system','task_type','status','assigned_to','deferred_to','created',)
    list_filter = ('status',)
    search_fields = ('task_title','system_reference_number',)
    inlines = [TaskOwnerAdminInline,TaskAssignmentAdminInline]

class TaskGroupAccessAdminInline(admin.TabularInline):
    model = models.TaskGroupAccess
    #raw_id_fields = ('user',)
    extra = 0

@admin.register(models.TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name','created',)
    list_filter = ('group_name',)
    search_fields = ('group_name',)
    inlines = [TaskGroupAccessAdminInline,]

class TaskEscalationAssignmentAdminInline(admin.TabularInline):
    model = models.TaskEscalationAssignment
    extra = 0

@admin.register(models.TaskEscalation)
class TaskEscalationAdmin(admin.ModelAdmin):
    list_display = ('task','esculation_dt','created',)
    search_fields = ('task',)
    inlines = [TaskEscalationAssignmentAdminInline]








#@admin.register(models.TaskGroupAccess)
#class TaskGroupAccessAdmin(admin.ModelAdmin):
#    raw_id_fields = ('user',)
#    list_display = ('task_group','user','created',)
#    list_filter = ('task_group',)
#    search_fields = ('task_group',)
#


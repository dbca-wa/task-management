from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.db.models import Q

from ledger.accounts import admin as ledger_admin
from ledger.accounts.models import EmailUser
from copy import deepcopy

from taskmanagement import models

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title','system_reference_number','system','task_type','status','assigned_to','deferred_to','created',)
    list_filter = ('status',)
    search_fields = ('task_title','system_reference_number',)



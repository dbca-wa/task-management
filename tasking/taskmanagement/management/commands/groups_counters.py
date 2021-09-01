from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import timedelta
from taskmanagement import models
from ledger_api_client import models as ledgergw_models
from taskmanagement import common
import urllib.request, json


class Command(BaseCommand):
    help = 'Task Group Counter'

    def handle(self, *args, **options):
        print ("IMPORT LEDGER GROUP")
        json_response = {}
        models.GroupCounter.objects.all().delete()
        # ledger task group counters
        if ledgergw_models.DataStore.objects.filter(key_name='ledger_groups').count() > 0:
             ledger_groups = ledgergw_models.DataStore.objects.filter(key_name='ledger_groups')[0]
             for lgkeys in ledger_groups.data:
                 if 'groups_list' in lgkeys:
                      for lg in ledger_groups.data['groups_list']:
                           common.updateTaskGroupCounter(lg['group_id'], 2)

        # taskmanagement task group counters

        task_groups = models.TaskGroup.objects.all()
        for tg in task_groups:
             common.updateTaskGroupCounter(tg.id, 0)

        # User counters
        users = ledgergw_models.EmailUser.objects.all()
        for u in users:
             common.updateTaskGroupCounter(u.ledger_id, 1)

             

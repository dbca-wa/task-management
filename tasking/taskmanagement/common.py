from taskmanagement import models
from django.db.models import Q, Min
import datetime
import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def person_group_type(pg_type):

    if pg_type == 'emailuser':
         return 1 
    if pg_type == 'taskgroup':
         return 0
    if pg_type == 'ledgergroup':
         return 2

    return None



def build_groups(request):
   
    print ("build_groups")
    ledger_group = {}
    task_group = {}
    gc = models.GroupCounter.objects.filter(Q(group_type=0) | Q(group_type=2))

    for i in gc:
        print (i)
        if i.group_type == 2:
            ledger_group[i.group_id] = i.total
        if i.group_type == 0:
            task_group[i.group_id] = i.total


    list_groups = [] 
    if request.user.is_authenticated:
         if request.user.ledger_groups is not None:
              ledger_groups = request.user.ledger_groups
              for lg in ledger_groups:
                     total = -10
                     if lg['group_id'] in ledger_group:
                        total = ledger_group[lg['group_id']]

                     list_groups.append({'group_name': lg['group_name'],'group_type_id': 2,'group_type': 'ledgergroup', 'group_id': lg['group_id'],'total': total })
  
         if request.user.ledger_id is not None:
              if request.user.ledger_id > 0:
                   tg = models.TaskGroupAccess.objects.filter(user_id=request.user.ledger_id).values('task_group__id','task_group__group_name') 
                   for i in tg:
                        total = -10
                        if i['task_group__id'] in task_group:
                            total = task_group[i['task_group__id']]
                        list_groups.append({'group_name': i['task_group__group_name'],'group_type_id': 0,'group_type': 'ledgergroup', 'group_id': i['task_group__id'],'total': total })

         






    return list_groups



def updateTaskGroupCounter(task_group_id, task_group_type):
     now = datetime.datetime.now()

     total = models.TaskAssignment.objects.filter(assignment_group=task_group_type, assignment_value=task_group_id, task__deferred_to__lte=now).count()

     if models.GroupCounter.objects.filter(group_type=task_group_type,group_id=task_group_id).count() > 2:
          # Delete Duplicate Entries
          models.GroupCounter.objects.filter(group_type=task_group_type,group_id=task_group_id).delete()

     # create update group in counters table
     if models.GroupCounter.objects.filter(group_type=task_group_type,group_id=task_group_id).count() > 0:
         models.GroupCounter.objects.filter(group_type=task_group_type,group_id=task_group_id).update(total=total)
     else:
         models.GroupCounter.objects.create(group_type=task_group_type,group_id=task_group_id,total=total)





def buildTaskTable(request, context, results, task_model_type):
        tasks_list = []
        for t in results:
                task = {}
                if task_model_type == 'TaskAssignment':
                    task['id'] = t['task__id']
                    task['task_title'] = t['task__task_title']
                    task['task_description'] = t['task__task_description']
                    task['system_reference_number'] = t['task__system_reference_number']
                    task['system'] = t['task__system']
                    task['task_type'] = t['task__task_type']
                    task['status'] = t['task__status']
                    task['assigned_to'] = t['task__assigned_to']
                    task['deferred_to'] = t['task__deferred_to']
                    task['created'] = t['task__created']
                elif task_model_type == 'Task':
                    task['id'] = t['id']
                    task['task_title'] = t['task_title']
                    task['task_description'] = t['task_description']
                    task['system_reference_number'] = t['system_reference_number']
                    task['system'] = t['system']
                    task['task_type'] = t['task_type']
                    task['status'] = t['status']
                    task['assigned_to'] = t['assigned_to']
                    task['deferred_to'] = t['deferred_to']
                    task['created'] = t['created']


                tasks_list.append(task)
        # Pagination Totals
        page=1
        pagination = []
        paginationcount =1
        numberofpages = context['task_total'] / context['rowlimit']

        if numberofpages > int(numberofpages):
             numberofpages = int(numberofpages) + 1
        else:
             numberofpages = int(numberofpages)

        page = 1
        start = 0
        active = False
        prevpage = {}
        nextpage = {}
        prevdisabled = False
        nextdisabled = False
        while page <= numberofpages:
            if start == context['startrow']:
                active = True
                if page == 1:
                     prevdisabled = True
                if page == numberofpages:
                     nextdisabled = True

                prevpage = {'start': start - context['rowlimit'], 'limit': context['rowlimit'], 'disabled': prevdisabled}
                nextpage = {'start': start + context['rowlimit'], 'limit': context['rowlimit'], 'disabled': nextdisabled}

            pagination.append({'page': page, 'start': start, 'limit': context['rowlimit'], 'active': active})

            active = False
            page += 1
            start = start + context['rowlimit']

        context['startrowreal'] = context['startrow'] + 1
        context['tasks'] = tasks_list
        context['pagination'] = pagination
        context['prevpage'] = prevpage
        context['nextpage'] = nextpage
        return context


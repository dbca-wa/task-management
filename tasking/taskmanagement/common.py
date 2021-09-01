from taskmanagement import models
from django.db.models import Q, Min
from ledger_api_client import models as ledger_api_models
from ledger_api_client import common as ledger_api_common


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
                    task['task_type_name'] = models.Task.TASK_TYPE[t['task__task_type']]
                    task['status'] = t['task__status']
                    task['priority'] = t['task__task_priority']
                    task['assigned_to'] = t['task__assigned_to']
                    task['deferred_to'] = t['task__deferred_to']
                    task['created'] = t['task__created']
                    if t['task__assigned_to'] is None:
                          t['task__assigned_to'] = 0
                    if t['task__assigned_to'] > 0:
                        task['assigned_to_info'] = ledger_person_info(t['task__assigned_to'])
                    else:
                        task['assigned_to_info'] = None

                elif task_model_type == 'Task':
                    task['id'] = t['id']
                    task['task_title'] = t['task_title']
                    task['task_description'] = t['task_description']
                    task['system_reference_number'] = t['system_reference_number']
                    task['system'] = t['system']
                    task['task_type'] = t['task_type']
                    task['status'] = t['status']
                    task['priority'] = t['task_priority']
                    task['assigned_to'] = t['assigned_to']
                    task['deferred_to'] = t['deferred_to']
                    task['created'] = t['created']
                    if t['assigned_to'] is None:
                         t['assigned_to'] = 0
                    if t['assigned_to'] > 0:
                         task['assigned_to_info'] = ledger_person_info(t['assigned_to'])
                    else:
                         task['assigned_to_info'] = None

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
        prevpage = {'start': 0, 'limit': 0, 'disabled': True}
        nextpage = {'start': 0, 'limit': 0, 'disabled': True}
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


def loggedin_ledger_userinfo(request):
    item = None
    if request.user:
        if request.user.ledger_id:
            assignment_value = request.user.ledger_id

            item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': 'Unknown ('+str(assignment_value)+')', 'title2': '', 'title3': '', 'ledger_id': str(assignment_value)}
            if ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value)).count() > 0:
                  lm = ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value))[0]
                  item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': lm.first_name+' '+lm.last_name, 'title2': '', 'title3': '', 'ledger_id': str(assignment_value)}
            else:
                results = ledger_api_common.get_ledger_user_info_by_id(str(assignment_value))
                if results['status'] == 200:
                    item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': results['user']['first_name']+' '+results['user']['last_name'], 'title2': results['user']['email'], 'title3': '', 'id': str(-1000)}
    return item




def loggedin_userinfo_dropdown(request):
    item = None 
    if request.user:
        if request.user.ledger_id:
            assignment_value = request.user.ledger_id

            item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': 'Unknown ('+str(assignment_value)+')', 'title2': '', 'title3': '', 'id': str(assignment_value)+':emailuser'}
            if ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value)).count() > 0:
                  lm = ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value))[0]
                  item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': lm.first_name+' '+lm.last_name, 'title2': '', 'title3': '', 'id': str(assignment_value)+':emailuser'}
            else:
                results = ledger_api_common.get_ledger_user_info_by_id(str(assignment_value))
                if results['status'] == 200:
                    item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': results['user']['first_name']+' '+results['user']['last_name'], 'title2': results['user']['email'], 'title3': '', 'id': str(assignment_value)+':emailuser'}
    return item
    

def ledger_person_info(assignment_value):
    item = {}
    if ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value)).count() > 0:
          lm = ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value))[0]
          item = {'first_name':lm.first_name,'last_name':lm.last_name,'full_name': lm.first_name+' '+lm.last_name, 'id': int(assignment_value), 'email': lm.email}
    else:
        results = ledger_api_common.get_ledger_user_info_by_id(str(assignment_value))
        if results['status'] == 200:
            item = {'first_name':results['user']['first_name'],'last_name':results['user']['last_name'],'full_name': results['user']['first_name']+' '+results['user']['last_name'], 'id': int(assignment_value), 'email': results['user']['email']}
    return item


def assignmentFriendlty(assignment_group,assignment_value):
    print('assignmentFriendlty')
    print (str(assignment_group) + " "+ str(assignment_value))
    item = {}
    if assignment_group == 0:
        item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': 'Unknown ('+str(assignment_value)+')', 'title2': '', 'title3': '', 'id': str(assignment_value)+':taskgroup'}
        if models.TaskGroup.objects.filter(id=int(assignment_value)).count() > 0:
              tg = models.TaskGroup.objects.filter(id=int(assignment_value))[0]
              item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': tg.group_name, 'title2': '', 'title3': '', 'id': str(assignment_value)+':taskgroup'}
        # Task Group
        pass
    elif assignment_group == 1:
        item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': 'Unknown ('+str(assignment_value)+')', 'title2': '', 'title3': '', 'id': str(assignment_value)+':emailuser'}
        if ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value)).count() > 0:
              lm = ledger_api_models.EmailUser.objects.filter(ledger_id=int(assignment_value))[0]
              item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': lm.first_name+' '+lm.last_name, 'title2': '', 'title3': '', 'id': str(assignment_value)+':emailuser'}
        else:
            results = ledger_api_common.get_ledger_user_info_by_id(str(assignment_value))
            if results['status'] == 200:
                item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': results['user']['first_name']+' '+results['user']['last_name'], 'title2': results['user']['email'], 'title3': '', 'id': str(assignment_value)+':emailuser'}

        # Task Person (ledger)
        pass
    elif assignment_group == 2:
        # Task Ledger Group (ledger)
        item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': 'Unknown ('+str(assignment_value)+')', 'title2': '', 'title3': '', 'id': str(assignment_value)+':ledgergroup'}
        if ledger_api_models.DataStore.objects.filter(key_name='ledger_groups').count() > 0:
             ds = ledger_api_models.DataStore.objects.filter(key_name='ledger_groups')[0]
             ledger_groups = ds.data
             for lg in ledger_groups['groups_list']:
                 if int(assignment_value) == int(lg['group_id']):
                     item = {'icon': '/static/images/group_person_icon_wh.png', 'title1': lg['group_name'], 'title2': '', 'title3': '', 'id': str(assignment_value)+':ledgergroup'}
 
    return item

def task_owner_multiselect(task_id):
    item_array = []
    task_owners = models.TaskOwner.objects.filter(task__id=task_id)
    for to in task_owners:
         item = assignmentFriendlty(to.assignment_group,to.assignment_value)
         item_array.append(item)
    return item_array

def task_assignment_multiselect(task_id):
    item_array = []
    item_list = models.TaskAssignment.objects.filter(task__id=task_id)
    for i in item_list:
         item = assignmentFriendlty(i.assignment_group,i.assignment_value)
         item_array.append(item)
    return item_array

def task_esculation_multiselect(task_id):
    item_array = []
    item_list = models.TaskEscalationAssignment.objects.filter(task__id=task_id)
    for i in item_list:
         item = assignmentFriendlty(i.assignment_group,i.assignment_value)
         item_array.append(item)
    return item_array

def get_extension_from_filename(filename):
    if filename[-4:-3] == '.':
       return filename[-3:]
    if filename[-5:-4] == '.':
       return filename[-4:]



##@python_2_unicode_compatible
#class TaskEscalation(models.Model):
#    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
#    esculation_dt = models.DateTimeField(null=True, blank=True)
#    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#
##@python_2_unicode_compatible
#class TaskEscalationAssignment(models.Model):
#    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
#    esculation = models.ForeignKey(TaskEscalation, blank=False, null=False, on_delete=models.CASCADE,)
#    assignment_group = models.IntegerField(choices=ASSIGNMENT_GROUP,default=-1)
#    assignment_value = models.IntegerField(blank=False, null=False)
#    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#


##ASSIGNMENT_GROUP = (
#   (0, 'taskgroup'),
#      (1, 'emailuser'),
#         (2, 'ledgergroup'),
#         )
#



def common_log(line):
     dt = datetime.datetime.now()
     f= open(settings.BASE_DIR+"/logs/common.log","a+")
     f.write(str(dt.strftime('%Y-%m-%d %H:%M:%S'))+': '+line+"\r\n")
     f.close()





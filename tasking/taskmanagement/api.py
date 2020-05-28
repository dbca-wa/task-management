import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from taskmanagement import models
from ledger_api_client import models as ledger_api_models
from ledger_api_client import common as ledger_api_common
from taskmanagement import common
import datetime
#from ledger.accounts.models import EmailUser


@csrf_exempt
#@require_http_methods(['POST'])
def search_pg(request, *args, **kwargs):
    """Search people and groups"""
    keyword = ''
    if request.GET.get('keyword'): 
         keyword = request.GET.get('keyword')

    data = {
    }
    data_list = []


    search_filter = Q()
    query_str_split = keyword.split()
    search_filter |= Q(email__icontains=keyword)
    #print (query_str_split)

    for se_wo in query_str_split:
         search_filter |= Q(first_name__icontains=se_wo) | Q(last_name__icontains=se_wo)
    lresults = []
    try:
        lresults = ledger_api_common.search_ledger_users(keyword) 
    except Exception as e:
        common.common_log(str(e))

    lresults = ledger_api_common.search_ledger_users(keyword)
    if lresults['status'] == 200:
        for p in lresults['users']:
            data_list.append({'icon': '/static/images/person_icon_wh.png', 'email': p['email'], 'title1': str(p['first_name'])+' '+str(p['last_name']), 'title2': p['email'], 'title3': '', 'id': str(p['ledgerid'])+':emailuser'})

    #print (search_filter)
#    for p in ledger_api_models.EmailUser.objects.filter(search_filter)[:10]:
#         data_list.append({'icon': '/static/images/person_icon_wh.png', 'email': p.email, 'title1': p.first_name +' '+p.last_name, 'title2': p.email, 'title3': '', 'id': str(p.ledger_id)+':emailuser'})

#    "icon": "/static/images/person_icon_wh.png",
#    "title1": "Jason Moore 1",
#    "title2": "Programmer 1",
#    "title3": "DBCA",
#    "id": "1:group"
#     
#  },
    
    ledger_groups = []
    if ledger_api_models.DataStore.objects.filter(key_name='ledger_groups').count() > 0:
         ds = ledger_api_models.DataStore.objects.filter(key_name='ledger_groups')[0]
         ledger_groups = ds.data
         for lg in ledger_groups['groups_list']:
             if keyword.lower() in lg['group_name'].lower():
                 data_list.append({'icon': '/static/images/group_person_icon_wh.png', 'title1': lg['group_name'], 'title2': '', 'title3': '', 'id': str(lg['group_id'])+':ledgergroup'})
    #print (ledger_groups['groups_list'])


    for g in Group.objects.filter(name__icontains=keyword)[:10]:
         data_list.append({'icon': '/static/images/group_person_icon_wh.png', 'title1': g.name, 'title2': '', 'title3': '', 'id': str(g.id)+':group'})
         #data_list.append({'name': g.name,})
 
    for g in models.TaskGroup.objects.filter(group_name__icontains=keyword)[:10]:
         data_list.append({'icon': '/static/images/task_group_wh.png', 'title1': g.group_name, 'title2': '', 'title3': '', 'id': str(g.id)+':taskgroup'})
 
    return HttpResponse(json.dumps(data_list), content_type='application/json')


@csrf_exempt
def create_task_comment(request, *args, **kwargs):
    data_list = {'status': 404, 'response_data': {"message": "Not Found"}}
    try:
        task_comment = request.POST.get('task_comment','')
        task_id = request.POST.get('task_id',None)
        task_status = request.POST.get('task_status',None)
        task_deferred_date = request.POST.get('task_deferred_date',None)
        ledger_info = common.loggedin_ledger_userinfo(request)
        task = models.Task.objects.get(id=int(task_id))
        models.TaskComment.objects.create(task=task,task_comment=task_comment, created_by=(ledger_info['ledger_id']))
        print ("STATUS")
        print (task_deferred_date)
        if task_status == 'close':
            task.status = 0
        if task_status == 'defer':
            task.status = 1

        task_deferred_date_cov =  datetime.datetime.strptime(str(task_deferred_date), '%d/%m/%Y %H:%M')
        task.deferred_to = task_deferred_date_cov
        task.save()
        data_list['status'] = 200
        data_list['response_data']['message'] = "Successfully Created"
    except:
        data_list['status'] = 500
        data_list['response_data']['message'] = "Error Submitting data to Server."
    return HttpResponse(json.dumps(data_list), content_type='application/json', status=data_list['status'])


#class TaskComment(models.Model):
#    task = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
#    task_comment = models.TextField(blank=True, null=True, default="")
#    created_by = models.IntegerField(blank=True, null=True)
#    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)



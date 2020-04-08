import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from taskmanagement import models
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
    #print (search_filter)
    #for p in EmailUser.objects.filter(search_filter)[:10]:
    #     data_list.append({'icon': '/static/images/person_icon_wh.png', 'email': p.email, 'title1': p.first_name +' '+p.last_name, 'title2': p.email, 'title3': '', 'id': str(p.id)+':emailuser'})

#    "icon": "/static/images/person_icon_wh.png",
#    "title1": "Jason Moore 1",
#    "title2": "Programmer 1",
#    "title3": "DBCA",
#    "id": "1:group"
#     
#  },

    for g in Group.objects.filter(name__icontains=keyword)[:10]:
         data_list.append({'icon': '/static/images/group_person_icon_wh.png', 'title1': g.name, 'title2': '', 'title3': '', 'id': str(g.id)+':group'})
         #data_list.append({'name': g.name,})
 
    for g in models.TaskGroup.objects.filter(group_name__icontains=keyword)[:10]:
         data_list.append({'icon': '/static/images/task_group_wh.png', 'title1': g.group_name, 'title2': '', 'title3': '', 'id': str(g.id)+':taskgroup'})

 
    return HttpResponse(json.dumps(data_list), content_type='application/json')


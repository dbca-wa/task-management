# Dajngo Imports
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.template import RequestContext
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Min

# Other
from taskmanagement import models 
from taskmanagement import forms as task_forms
from taskmanagement import common
import datetime
import json

class HomePage(TemplateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'home_page.html'
    def render_to_response(self, context):

        #if self.request.user.is_authenticated:
        #   if len(self.request.user.first_name) > 0:
        #       donothing = ''
        #   else:
        #       return HttpResponseRedirect(reverse('first_login_info_steps', args=(self.request.user.id,1)))
        template = get_template(self.template_name)
        #context = RequestContext(self.request)

        context['csrf_token_value'] = get_token(self.request)
        #results = models.Task.objects.all()

        startrow = 0
        rowlimit = 10
        if 'start' in self.request.GET:
            startrow=int(self.request.GET['start'])
        if 'limit' in self.request.GET:
            rowlimit =int(self.request.GET['limit'])
        context['startrow'] = startrow
        context['rowlimit'] = rowlimit
        rowend = rowlimit + startrow
        context['rowend'] = rowend
        results = models.Task.objects.all().values('id','task_title','task_description','system_reference_number','system','task_type','task_priority','status','assigned_to','deferred_to','created')[startrow:rowend]
        context['task_total'] = models.Task.objects.all().count()
        context = common.buildTaskTable(self.request, context, results,'Task')



        #context['tasks'] = results
        #context['task_total'] = results.count()
        context['messages'] = messages.get_messages(self.request)
        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['user'] = self.request.user
        if self.request.user.is_staff is True:
           context['staff'] = self.request.user.is_staff
        else:
           context['staff'] = False

        context['task_groups'] = common.build_groups(self.request)
        #context = template_context(self.request)
        return context

class EditTask(LoginRequiredMixin, UpdateView):
    template_name = 'body/edit_task.html'
    form_class = task_forms.NewTaskForm
    model = models.Task


    def get_context_data(self, **kwargs):
        context = super(EditTask, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(EditTask, self).get_initial()
        esculation_date_time = ''
        if models.TaskEscalation.objects.filter(task__id=self.object.pk).count() > 0:
            esculation_date_time = models.TaskEscalation.objects.filter(task__id=self.object.pk)[0].esculation_dt.strftime('%d/%m/%Y %H:%M')
        initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        initial['esculation_date_time'] = esculation_date_time
        initial['task_owner'] = json.dumps(common.task_owner_multiselect(self.object.pk))
        initial['task_assignments'] = json.dumps(common.task_assignment_multiselect(self.object.pk))
        initial['task_esculations'] = json.dumps(common.task_esculation_multiselect(self.object.pk))

        # [{"icon":"/static/images/group_person_icon_wh.png","title1":"Approver","title2":"","title3":"","id":"1:ledgergroup"}]
        return initial

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            app = self.get_object().application_set.first()
            return HttpResponseRedirect(app.get_absolute_url())
        return super(EditTask, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        forms_data = form.cleaned_data
        self.object.save()

        assignment_group=None
        esculation_date_time=None
        task_owners = []
        task_assignments = []
        task_esculations = []

        if common.is_json(self.request.POST.get('task_owner',[])) is True:
            task_owners = json.loads(self.request.POST.get('task_owner',[]))
        if common.is_json(self.request.POST.get('task_assignments',[])) is True:
            task_assignments = json.loads(self.request.POST.get('task_assignments',[]))
        if common.is_json(self.request.POST.get('task_esculations',[])) is True:
            task_esculations = json.loads(self.request.POST.get('task_esculations',[]))

        esculation_dt = self.request.POST.get('esculation_date_time',None)
        if esculation_dt is not None:
             esculation_date_time = datetime.datetime.strptime(self.request.POST.get('esculation_date_time',None), '%d/%m/%Y %H:%M')
        #esculation_date_time = self.request.POST.get('esculation_date_time',None)

        models.TaskOwner.objects.filter(task=self.object).delete()
        for to in task_owners:
            to_id = to['id']
            to_id_split =  to_id.split(":")
            #if to_id_split[1] == 'emailuser':
            assignment_group=common.person_group_type(to_id_split[1])
            to_obj = models.TaskOwner.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=int(to_id_split[0]))

        models.TaskAssignment.objects.filter(task=self.object).delete()
        for ta in task_assignments:
            ta_id = ta['id']
            ta_id_split =  ta_id.split(":")
            #if ta_id_split[1] == 'emailuser':
            assignment_group=common.person_group_type(ta_id_split[1])
            ta_obj = models.TaskAssignment.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=int(ta_id_split[0]))
            common.updateTaskGroupCounter(int(ta_id_split[0]), assignment_group)

        if models.TaskEscalation.objects.filter(task=self.object).count() == 1 :
            te_obj = models.TaskEscalation.objects.get(task=self.object)
            te_obj.esculation_dt = esculation_date_time
            te_obj.save()
        else:
            models.TaskEscalation.objects.filter(task=self.object).delete()
            te_obj = models.TaskEscalation.objects.create(task=self.object,esculation_dt=esculation_date_time)

        models.TaskEscalationAssignment.objects.filter(task=self.object).delete()
        for te in task_esculations:
            te_id = te['id']
            te_id_split =  te_id.split(":")
            assignment_group=common.person_group_type(te_id_split[1])
            ta_obj = models.TaskEscalationAssignment.objects.create(task=self.object,esculation=te_obj,assignment_group=assignment_group,assignment_value=int(te_id_split[0]))
            

        return HttpResponseRedirect(reverse('home_page',))

class AssignTask(LoginRequiredMixin, UpdateView):
    template_name = 'body/assign_task.html'
    form_class = task_forms.AssignTaskForm
    model = models.Task


    def get_context_data(self, **kwargs):
        context = super(AssignTask, self).get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super(AssignTask, self).get_initial()
        assigned_to_var = []
        assigned_to_current_loggedin = common.loggedin_userinfo_dropdown(self.request)
        if assigned_to_current_loggedin:
             assigned_to_var.append(assigned_to_current_loggedin)
        #print ("LEDGERID")
        #print (initial['assigned_to'])
        #print (self.request.user.ledger_id)
        initial['assigned_to'] = json.dumps(assigned_to_var)
        #esculation_date_time = ''
        #if models.TaskEscalation.objects.filter(task__id=self.object.pk).count() > 0:
        #    esculation_date_time = models.TaskEscalation.objects.filter(task__id=self.object.pk)[0].esculation_dt.strftime('%d/%m/%Y %H:%M')
        #initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        #initial['esculation_date_time'] = esculation_date_time
        #initial['task_owner'] = json.dumps(common.task_owner_multiselect(self.object.pk))
        #initial['task_assignments'] = json.dumps(common.task_assignment_multiselect(self.object.pk))
        #initial['task_esculations'] = json.dumps(common.task_esculation_multiselect(self.object.pk))

        # [{"icon":"/static/images/group_person_icon_wh.png","title1":"Approver","title2":"","title3":"","id":"1:ledgergroup"}]
        return initial

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            app = self.get_object().application_set.first()
            return HttpResponseRedirect(app.get_absolute_url())
        return super(AssignTask, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        print ("FORM VALID")
        self.object = form.save(commit=False)
        forms_data = form.cleaned_data
        print ("ASSIGN TASK DATA")
        print (forms_data)
        assigned_to = json.loads(self.request.POST.get('assigned_to',[]))
        if len(assigned_to) > 0:
            if 'id' in assigned_to:
                  at_split = assigned_to['id'].split(":")
                  self.object.assigned_to = int(at_split[0])
        print (self.request.POST.get('assigned_to',None))
        self.object.save()
        return HttpResponseRedirect(reverse('home_page',))


class NewTask(LoginRequiredMixin, CreateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'body/new_task.html'
    form_class = task_forms.NewTaskForm
    model = models.Task

#    def render_to_response(self, context):
#
#        #if self.request.user.is_authenticated:
#        #   if len(self.request.user.first_name) > 0:
#        #       donothing = ''
#        #   else:
#        #       return HttpResponseRedirect(reverse('first_login_info_steps', args=(self.request.user.id,1)))
#        template = get_template(self.template_name)
#        context = RequestContext(self.request, context)
#        context['csrf_token_value'] = get_token(self.request)
#        context['tasks'] = models.Task.objects.all()
#        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(NewTask, self).get_context_data(**kwargs)
#        context['request'] = self.request
#        context['user'] = self.request.user
#        if self.request.user.is_staff is True:
#           context['staff'] = self.request.user.is_staff
#        else:
#           context['staff'] = False

        #context = template_context(self.request)
        return context

    def get_initial(self):
        initial = super(NewTask, self).get_initial()
        initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        return initial

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            app = self.get_object().application_set.first()
            return HttpResponseRedirect(app.get_absolute_url())
        return super(NewTask, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        forms_data = form.cleaned_data
        self.object.save()

        assignment_group=None
        esculation_date_time=None
        task_owners = []
        task_assignments = []
        task_esculations = []

        if common.is_json(self.request.POST.get('task_owner',[])) is True: 
            task_owners = json.loads(self.request.POST.get('task_owner',[]))
        if common.is_json(self.request.POST.get('task_assignments',[])) is True:
            task_assignments = json.loads(self.request.POST.get('task_assignments',[]))
        if common.is_json(self.request.POST.get('task_esculations',[])) is True:
            task_esculations = json.loads(self.request.POST.get('task_esculations',[]))

        esculation_dt = self.request.POST.get('esculation_date_time',None)
        if esculation_dt is not None:
             esculation_date_time = datetime.datetime.strptime(self.request.POST.get('esculation_date_time',None), '%d/%m/%Y %H:%M')
        for to in task_owners:
            to_id = to['id']
            to_id_split =  to_id.split(":")
            assignment_group=common.person_group_type(to_id_split[1])
            to_obj = models.TaskOwner.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=int(to_id_split[0]))

        for ta in task_assignments:
            ta_id = ta['id']
            ta_id_split =  ta_id.split(":")
            assignment_group=common.person_group_type(ta_id_split[1])
            ta_obj = models.TaskAssignment.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=int(ta_id_split[0]))
            common.updateTaskGroupCounter(int(ta_id_split[0]), assignment_group)

        te_obj = models.TaskEscalation.objects.create(task=self.object,esculation_dt=esculation_date_time)
        for te in task_esculations:
            te_id = te['id']
            te_id_split =  te_id.split(":")
            assignment_group=common.person_group_type(te_id_split[1])
            ta_obj = models.TaskEscalationAssignment.objects.create(task=self.object,esculation=te_obj,assignment_group=assignment_group,assignment_value=int(te_id_split[0]))

        return HttpResponseRedirect(reverse('home_page',))
#  (0, 'taskgroup'),
#   (1, 'emailuser'),
#   (2, 'groups'),


# {'status': 1, 'task_esculations': '[{"email":"jason.moore@dbca.wa.gov.au","title1":"Jason Moore","title2":"jason.moore@dbca.wa.gov.au","id":"1:emailuser","icon":"/static/images/person_icon_wh.png","title3":""}]', 'task_owner': '[{"email":"jason.moore@dbca.wa.gov.au","title1":"Jason Moore","title2":"jason.moore@dbca.wa.gov.au","id":"1:emailuser","icon":"/static/images/person_icon_wh.png","title3":""}]', 'task_assignments': '[{"email":"jason.moore@dbca.wa.gov.au","title1":"Jason Moore","title2":"jason.moore@dbca.wa.gov.au","id":"1:emailuser","icon":"/static/images/person_icon_wh.png","title3":""}]', 'task_type': 0, 'task_title': 'oim 2', 'task_description': 'DASASFAS', 'deferred_to': datetime.datetime(2020, 3, 12, 17, 44, 48, tzinfo=<DstTzInfo 'Australia/Perth' AWST+8:00:00 STD>)}


#        self.object = form.save(commit=False)
#        forms_data = form.cleaned_data
#        pk = self.kwargs['pk']
#        cg = ChangeGroup.objects.get(pk=pk)
##        cpp = ChangePricePeriod.objects.create(days=forms_data['days'],calulation_type=forms_data['calulation_type'], amount=forms_data['amount'], percentage=forms_data['percentage'])
#        self.object.save()
#        cg.change_period.add(self.object)
#        cg.save()



class ViewTask(LoginRequiredMixin, DetailView):
    # preperation to replace old homepage with screen designs..

    template_name = 'body/view_task.html'
    #form_class = task_forms.NewTaskForm
    model = models.Task

#    def render_to_response(self, context):
#
#        #if self.request.user.is_authenticated:
#        #   if len(self.request.user.first_name) > 0:
#        #       donothing = ''
#        #   else:
#        #       return HttpResponseRedirect(reverse('first_login_info_steps', args=(self.request.user.id,1)))
#        template = get_template(self.template_name)
#        context = RequestContext(self.request, context)
#        context['csrf_token_value'] = get_token(self.request)
#        context['tasks'] = models.Task.objects.all()
#        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(ViewTask, self).get_context_data(**kwargs)
        task_id = self.kwargs['pk']
        task = models.Task.objects.get(id=int(task_id))
        task_comments = models.TaskComment.objects.filter(task=task)
        context['current_datetime'] = datetime.datetime.now()
        context['task_comments'] = []
        for tc in task_comments:
            row = {}
            row['id'] = tc.id
            row['comment'] = tc.task_comment
            row['created_by_id'] = tc.created_by
            if tc.created_by:
               ledger_info = common.assignmentFriendlty(1,int(tc.created_by))
               row['created_by_name'] = ledger_info['title1']
            else:
               row['created_by_name'] = "Unknown"
            row['created'] = tc.created
            row['comment_attachments'] = []
            comment_attachments =  models.TaskCommentAttachment.objects.filter(task_comment=tc)
            for ca in comment_attachments:
                ca_row = {}
                ca_row['id'] = ca.id
                ca_row['upload'] = ca.upload.path
                ca_row['filename'] = ca.filename
                ca_row['extension'] = ca.extension
                row['comment_attachments'].append(ca_row)


            context['task_comments'].append(row) 
        #context['']
#        context['request'] = self.request
#        context['user'] = self.request.user
#        if self.request.user.is_staff is True:
#           context['staff'] = self.request.user.is_staff
#        else:
#           context['staff'] = False

        #context = template_context(self.request)
        return context

    def get_initial(self):
        initial = super(ViewTask, self).get_initial()
        initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        return initial



class MyTaskAssignments(LoginRequiredMixin, TemplateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'body/my_task_assignments.html'
    model = models.Task

    def get_context_data(self, **kwargs):
        context = super(MyTaskAssignments, self).get_context_data(**kwargs)
        filter_query = Q()
        now = datetime.datetime.now()

        if self.request.user:
           if self.request.user.ledger_id:
               # User Specific
               ledger_id = self.request.user.ledger_id
               filter_query |= Q(assignment_value=ledger_id, assignment_group=1)

               # Task Group Specific
               task_groups = models.TaskGroupAccess.objects.filter(user_id=ledger_id).values('task_group__id')
               for tg in task_groups:
                   filter_query |= Q(assignment_value=tg['task_group__id'], assignment_group=0)

           if self.request.user.ledger_groups:
               print ("MyTaskAssignmentsGroups")
               for lg in self.request.user.ledger_groups:
                   filter_query |= Q(assignment_value=lg['group_id'], assignment_group=2)
           
              
        filter_query &= Q(task__deferred_to__lte=now)


        startrow = 0
        rowlimit = 10
        if 'start' in self.request.GET:
            startrow=int(self.request.GET['start'])
        if 'limit' in self.request.GET:
            rowlimit =int(self.request.GET['limit'])
        context['startrow'] = startrow
        context['rowlimit'] = rowlimit
        rowend = rowlimit + startrow 
        context['rowend'] = rowend
        results = models.TaskAssignment.objects.filter(filter_query).values('task__id','task__task_title','task__task_description','task__system_reference_number','task__system','task__task_type','task__status','task__assigned_to','task__task_priority','task__deferred_to','task__created')[startrow:rowend]
        print (results.query)
        context['task_total'] = models.TaskAssignment.objects.filter(filter_query).count()
        context = common.buildTaskTable(self.request, context, results,'TaskAssignment')

        # Task Group Bar ( Top ) 
        context['task_groups'] = common.build_groups(self.request)
        return context

    def get_initial(self):
        initial = super(MyTaskAssignments, self).get_initial()
        #initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return initial


#    task_title = models.CharField(max_length=256)
#    task_description = models.TextField(blank=True, null=True, default="")
#    system_reference_number = models.CharField(max_length=256)
#    system = models.ForeignKey(System, blank=True, null=True, on_delete=models.CASCADE,)
#    task_type = models.IntegerField(choices=TASK_TYPE,default=-1)
#    #owner_role =
#    #assignment_role =
#    #esculation =
#    status = models.IntegerField(choices=TASK_STATUS,default=1)
#    assigned_to = models.IntegerField(blank=True, null=True)
#    deferred_to = models.DateTimeField(null=True, blank=True)
#    extra_meta = JSONField(null=True, blank=True)
#    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class MyAssignedTasks(LoginRequiredMixin, TemplateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'body/my_assigned_tasks.html'
    model = models.Task

    def get_context_data(self, **kwargs):
        context = super(MyAssignedTasks, self).get_context_data(**kwargs)

        filter_query = Q()

        if self.request.user:
           if self.request.user.ledger_id:
               # User Specific
               ledger_id = self.request.user.ledger_id
               filter_query |= Q(assigned_to=ledger_id)

        startrow = 0
        rowlimit = 10
        if 'start' in self.request.GET:
            startrow=int(self.request.GET['start'])
        if 'limit' in self.request.GET:
            rowlimit =int(self.request.GET['limit'])
        context['startrow'] = startrow
        context['rowlimit'] = rowlimit
        rowend = rowlimit + startrow 
        context['rowend'] = rowend
        results = models.Task.objects.filter(filter_query).values('id','task_title','task_description','system_reference_number','system','task_type','status','task_priority','assigned_to','deferred_to','created')[startrow:rowend]
        context['task_total'] = models.Task.objects.filter(filter_query).count()
        context = common.buildTaskTable(self.request, context, results,'Task')

        
#        for t in results:
#            task = {}
#            print (t)
#            task['id'] = t['id']
#            task['task_title'] = t['task_title']
#            task['task_description'] = t['task_description']
#            task['system_reference_number'] = t['system_reference_number']
#            task['system'] = t['system']
#            task['task_type'] = t['task_type']
#            task['status'] = t['status']
#            task['assigned_to'] = t['assigned_to']
#            task['deferred_to'] = t['deferred_to']
#            task['created'] = t['created']
#            tasks_list.append(task)
#
#        context['tasks'] = tasks_list
        context['task_groups'] = common.build_groups(self.request)
        return context

    def get_initial(self):
        initial = super(MyAssignedTasks, self).get_initial()
        #initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return initial


class GroupTasks(LoginRequiredMixin, TemplateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'body/tasks_groups.html'
    model = models.Task

    def get_context_data(self, **kwargs):
        context = super(GroupTasks, self).get_context_data(**kwargs)
        filter_query = Q()
        tasks_list = []
        showresults = False
        now = datetime.datetime.now()
        print ("GroupTasks")
        group_id = int(kwargs['pk'])
        group_type = int(kwargs['group_type'])
        ledger_id = -1000
        if self.request.user:
             if self.request.user.ledger_id:
                # User Specific
                ledger_id = self.request.user.ledger_id



        print ("GRO")
        if group_type == 0:
            if models.TaskGroupAccess.objects.filter(user_id=ledger_id, task_group__id=group_id).count() > 0: 
               filter_query |= Q(assignment_value=group_id, assignment_group=group_type) 
               showresults = True 

        if group_type == 2:
           if self.request.user.ledger_groups:
               print ("MyTaskAssignmentsGroups")
               for lg in self.request.user.ledger_groups:
                   if lg['group_id'] == group_id:
                        filter_query |= Q(assignment_value=lg['group_id'], assignment_group=2)
                        showresults = True



        if showresults == True:
             startrow = 0
             rowlimit = 10
             if 'start' in self.request.GET:
                 startrow=int(self.request.GET['start'])
             if 'limit' in self.request.GET:
                 rowlimit =int(self.request.GET['limit'])
             context['startrow'] = startrow
             context['rowlimit'] = rowlimit
             rowend = rowlimit + startrow
             context['rowend'] = rowend
             filter_query &= Q(task__deferred_to__lte=now)
             results = models.TaskAssignment.objects.filter(filter_query).values('task__id','task__task_title','task__task_description','task__system_reference_number','task__system','task__task_type','task__status','task__task_priority','task__assigned_to','task__deferred_to','task__created')[startrow:rowend]
             context['task_total'] = models.TaskAssignment.objects.filter(filter_query).count()
             context = common.buildTaskTable(self.request, context, results,'TaskAssignment')


        # Task Group Bar (Top)
        context['task_groups'] = common.build_groups(self.request)
        return context

    def get_initial(self):
        initial = super(GroupTasks, self).get_initial()
        #initial['deferred_to'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return initial



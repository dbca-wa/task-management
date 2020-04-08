# Dajngo Imports
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.template import RequestContext
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

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
        context['tasks'] = models.Task.objects.all()
        print ("WHAT ")
        print (context)
        print("NO")
        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['user'] = self.request.user
        if self.request.user.is_staff is True:
           context['staff'] = self.request.user.is_staff
        else:
           context['staff'] = False

        #context = template_context(self.request)
        return context


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
        print ("TASK_OWNER")

#        print (forms_data['task_owner'])
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

        print (task_owners)
        for to in task_owners:
            to_id = to['id']
            to_id_split =  to_id.split(":")
            #if to_id_split[1] == 'emailuser':
            assignment_group=common.person_group_type(to_id_split[1])
            to_obj = models.TaskOwner.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=to_id[0])

        for ta in task_assignments:
            ta_id = ta['id']
            ta_id_split =  ta_id.split(":")
            #if ta_id_split[1] == 'emailuser':
            assignment_group=common.person_group_type(ta_id_split[1])
            ta_obj = models.TaskAssignment.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=ta_id[0])


        te_obj = models.TaskEscalation.objects.create(task=self.object,esculation_dt=esculation_date_time)


#        for ta in task_assignments:
#            ta_id = ta['id']
#            ta_id_split =  ta_id.split(":")
#            if ta_id_split[1] == 'emailuser':
#                 assignment_group=1
#            ta_obj = models.TaskAssignment.objects.create(task=self.object,assignment_group=assignment_group,assignment_value=ta_id[0])
#
        print ("FORM DATA")
        print (forms_data)
        print ("POST")
        print (self.request.POST)
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


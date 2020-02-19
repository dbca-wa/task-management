# Dajngo Imports
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.template import RequestContext
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
# Other
from taskmanagement import models 
from taskmanagement import forms as task_forms


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
        context = RequestContext(self.request, context)
        context['csrf_token_value'] = get_token(self.request)
        context['tasks'] = models.Task.objects.all()
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
        return initial

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel'):
            app = self.get_object().application_set.first()
            return HttpResponseRedirect(app.get_absolute_url())
        return super(NewTask, self).post(request, *args, **kwargs)


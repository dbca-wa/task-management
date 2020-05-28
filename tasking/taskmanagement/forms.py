from __future__ import unicode_literals
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms import Form, ModelForm, ChoiceField, FileField, CharField, Textarea, ClearableFileInput, HiddenInput, Field, RadioSelect, ModelChoiceField, Select, DateTimeField
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from django import forms
import json
#from splitjson.widgets import SplitJSONWidget

#crispy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, MultiField, Div
from crispy_forms.bootstrap import FormActions, InlineRadios

# Other
#from ledger.accounts.models import EmailUser, Address, Organisation
#from ledger.accounts.models import EmailUser, Address, Organisation, Document, OrganisationAddress

from taskmanagement import models


User = get_user_model()


class BaseFormHelper(FormHelper):
    form_class = 'form-horizontal'
    label_class = 'col-xs-12 col-sm-12 col-md-12 col-lg-12'
    field_class = 'col-xs-12 col-sm-12 col-md-12 col-lg-12'

class NewTaskForm(ModelForm):

    task_owner = CharField(required=False, widget=Textarea(attrs={'style':'display:none',}), help_text='Task Owner',)
    task_assignments = CharField(required=False, widget=Textarea(attrs={'style':'display:none',}), help_text='Task Assignment')
    task_esculations = CharField(required=False, widget=Textarea(attrs={'style':'display:none',}), help_text='Task Esculations')
    esculation_date_time = DateTimeField() 

    class Meta:
        model = models.Task
        fields = ['task_title','task_description','task_type','task_priority','deferred_to']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        #user = kwargs.pop('user')
        super(NewTaskForm, self).__init__(*args, **kwargs)
        if kwargs['instance'] is not None:
             task_button = 'Update Task'
        else:
             task_button = 'Create Task'

        self.helper = BaseFormHelper()
        self.fields['deferred_to'].widget.attrs['autocomplete'] = 'off'
        self.fields['esculation_date_time'].widget.attrs['autocomplete'] = 'off'
        self.helper.add_input(Submit(task_button, task_button, css_class='btn-lg'))
        owner_selection = HTML("<BR>")#HTML('{% include "body/task_owner_selection.html" %}')
        self.helper.layout = Layout(owner_selection,'task_owner','task_title','task_description','task_type','task_priority','deferred_to','task_assignments','task_esculations','esculation_date_time')



class AssignTaskForm(ModelForm):

    assigned_to = CharField(required=False, widget=HiddenInput(attrs={'iistyle':'display:none',}), help_text='Assign To',)

    class Meta:
        model = models.Task
        fields = ['assigned_to',]

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        #user = kwargs.pop('user')
        super(AssignTaskForm, self).__init__(*args, **kwargs)
        task_button = 'Assign Task'
        print (self.fields)
        self.fields['assigned_to'].required = False
#        self.fields['task_title'].required = False
#        self.fields['task_description'].required = False

        self.render_required_fields = False
        self.helper = BaseFormHelper()
        #self.fields['assigned_to'].widget.attrs['autocomplete'] = 'off'
        self.helper.add_input(Submit(task_button, task_button, css_class='btn-lg'))
        owner_selection = HTML("<BR>")#HTML('{% include "body/task_owner_selection.html" %}')
        self.helper.layout = Layout(owner_selection,'assigned_to')

    def clean_assigned_to(self):
        print (self.cleaned_data['assigned_to'])
        print (len(self.cleaned_data['assigned_to']))
        json_assign_to = json.loads(self.cleaned_data['assigned_to']) 
        if len(json_assign_to) > 0:
            return True
        raise forms.ValidationError('Please select a valid assignment.') 
        return False


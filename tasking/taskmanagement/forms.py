from __future__ import unicode_literals
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms import Form, ModelForm, ChoiceField, FileField, CharField, Textarea, ClearableFileInput, HiddenInput, Field, RadioSelect, ModelChoiceField, Select, DateTimeField
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES

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
        fields = ['task_title','task_description','task_type','status', 'deferred_to']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        #user = kwargs.pop('user')
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['deferred_to'].widget.attrs['autocomplete'] = 'off'
        self.helper.add_input(Submit('Create Task', 'Create Task', css_class='btn-lg'))
        owner_selection = HTML("<BR>")#HTML('{% include "body/task_owner_selection.html" %}')
        self.helper.layout = Layout(owner_selection,'task_owner','task_title','task_description','task_type','status', 'deferred_to','task_assignments','task_esculations','esculation_date_time')



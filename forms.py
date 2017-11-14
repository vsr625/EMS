import datetime

from django import forms
from django.core.validators import MinLengthValidator
from django.db.models import Q
from django.forms import ModelForm
from django.template import Template

from .models import Participant, Event, Faculty, SpecialGuest, Coordinator


class RegisterParticipant(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       validators=[MinLengthValidator(8)])
    field_order = ['Name', 'Password', 'confirm_password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']
    template = Template("""
        {% load material_form %}
        {% part form.Name prefix %}<i class="material-icons prefix">account_box</i>{% endpart %}
        {% part form.MailId prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.Password prefix %}<i class="material-icons prefix">lock_open</i>
        {% endpart %}
        {% part form.confirm_password prefix %}<i class="material-icons prefix">lock_open</i>
        {% endpart %}
        {% part form.City prefix %}<i class="material-icons prefix">location_city</i>
        {% endpart %}
        {% part form.PhoneNo prefix %}<i class="material-icons prefix">phone</i>
        {% endpart %}
        {% part form.College prefix %}<i class="material-icons prefix">account_balance</i>
        {% endpart %}
        {% part form.RegNo prefix %}<i class="material-icons prefix">info</i> {% endpart %}
    """)

    class Meta:
        model = Participant
        fields = ['Name', 'Password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']
        widgets = {
            'Password': forms.PasswordInput(),
            'PhoneNo': forms.NumberInput(),
        }

    def clean(self):
        cleaned_data = super(RegisterParticipant, self).clean()
        password = cleaned_data.get("Password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Entered passwords does not match"
            )


class Login(forms.Form):
    username = forms.CharField(label="Enter Mail Id", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=False)
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EventForm(ModelForm):
    Coordinator = forms.ModelMultipleChoiceField(queryset=Coordinator.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple(),
                                                 required=False)
    template = Template(""" 
        {% load material_form %}
        {% part form.Name prefix %} <i class="material-icons prefix">account_box</i> {% endpart %}
        {% part form.Date prefix %} <i class="material-icons prefix">event</i> {% endpart %}
        {% part form.Time prefix %} <i class="material-icons prefix">access_time</i> {% endpart %}
        {% part form.Venue prefix %} <i class="material-icons prefix">place</i> {% endpart %}
        {% part form.RegistrationFee prefix %} <i class="material-icons prefix">attach_money</i> {% endpart %}
        {% part form.Prize prefix %} <i class="material-icons prefix">bookmark</i> {% endpart %}
        {% part form.Judge prefix %} <i class="material-icons prefix">account_balance</i> {% endpart %}
        {% part form.SpecialGuest prefix %} <i class="material-icons prefix">supervisor_account</i> {% endpart %}
    """)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['SpecialGuest'].queryset = SpecialGuest.objects.filter(
            Q(special_guest__isnull=True) | Q(special_guest=self.instance))
        # Don't know why only this works here

    class Meta:
        model = Event
        fields = ['Name', 'Date', 'Time', 'Venue', 'RegistrationFee', 'Prize', 'Judge', 'SpecialGuest']

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        date = cleaned_data.get('Date')
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")


class FacultyForm(ModelForm):
    template = Template(""" 
        {% load material_form %}
        {% part form.Name prefix %} <i class="material-icons prefix">account_box</i> {% endpart %}
        {% part form.PhoneNo prefix %}<i class="material-icons prefix">phone</i>  {% endpart %}
        {% part form.MailId prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.RegNo prefix %}<i class="material-icons prefix">info</i> {% endpart %}
    """)

    class Meta:
        model = Faculty
        fields = ['Name', 'PhoneNo', 'MailId', 'RegNo']
        widgets = {
            'PhoneNo': forms.NumberInput()
        }


class SPForm(ModelForm):
    template = Template(""" 
        {% load material_form %}
        {% part form.Name prefix %} <i class="material-icons prefix">account_box</i> {% endpart %}
        {% part form.PhoneNo prefix %}<i class="material-icons prefix">phone</i>  {% endpart %}
        {% part form.MailId prefix %}<i class="material-icons prefix">email</i>{% endpart %}
    """)
    class Meta:
        model = SpecialGuest
        fields = ['Name', 'PhoneNo', 'MailId']
        widgets = {
            'PhoneNo': forms.NumberInput()
        }


class UpdateWinner(ModelForm):
    def __init__(self, *args, **kwargs):
        e = kwargs.pop('e', None)
        super(UpdateWinner, self).__init__(*args, **kwargs)
        if e is not None:
            self.fields['Winner'] = forms.ModelChoiceField(queryset=e,
                                                           widget=forms.Select())

    class Meta:
        model = Event
        fields = ['Name', 'Winner']
        widgets = {
            'Name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class CoordinatorForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       validators=[MinLengthValidator(8)])
    field_order = ['Name', 'MailId', 'RegNo', 'Password', 'confirm_password']
    template = Template(""" 
        {% load material_form %}
        {% part form.Name prefix %} <i class="material-icons prefix">account_box</i> {% endpart %}
        {% part form.PhoneNo prefix %}<i class="material-icons prefix">phone</i>  {% endpart %}
        {% part form.MailId prefix %}<i class="material-icons prefix">email</i>{% endpart %}
        {% part form.RegNo prefix %}<i class="material-icons prefix">info</i> {% endpart %}
        {% part form.Password prefix %}<i class="material-icons prefix">lock_open</i>{% endpart %}
        {% part form.confirm_password prefix %}<i class="material-icons prefix">lock_open</i>{% endpart %}
    """)
    class Meta:
        model = Coordinator
        fields = ['Name', 'RegNo', 'Password', 'PhoneNo', 'MailId']
        widgets = {
            'Password': forms.PasswordInput(),
            'PhoneNo': forms.NumberInput()
        }

    def clean(self):
        cleaned_data = super(CoordinatorForm, self).clean()
        password = cleaned_data.get("Password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Entered passwords does not match"
            )

import datetime

from django import forms
from django.core.validators import MinLengthValidator
from django.db.models import Q
from django.forms import ModelForm

from .models import Participant, Event, Faculty, SpecialGuest, Coordinator


class RegisterParticipant(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       validators=[MinLengthValidator(8)])
    field_order = ['Name', 'Password', 'confirm_password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']

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
    class Meta:
        model = Faculty
        fields = ['Name', 'PhoneNo', 'MailId', 'RegNo']
        widgets = {
            'PhoneNo': forms.NumberInput()
        }


class SPForm(ModelForm):
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

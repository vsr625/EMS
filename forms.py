from django import forms
from django.core.validators import MinLengthValidator
from django.db.models import Q
from django.forms.utils import ErrorList

from .models import Participant, Event, Faculty, SpecialGuest, Coordinator, EventParticipates
from django.forms import ModelForm


class RegisterParticipant(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       validators=[MinLengthValidator(8)])
    field_order = ['Name', 'Password', 'confirm_password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']

    class Meta:
        model = Participant
        fields = ['Name', 'Password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']
        widgets = {
            'Password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'MailId': forms.EmailInput(attrs={'class': 'form-control'}),
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'PhoneNo': forms.NumberInput(attrs={'class': 'form-control'}),
            'College': forms.TextInput(attrs={'class': 'form-control'}),
            'RegNo': forms.TextInput(attrs={'class': 'form-control'}),
            'City': forms.TextInput(attrs={'class': 'form-control'})
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
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'RegistrationFee': forms.NumberInput(attrs={'class': 'form-control'}),
            'Prize': forms.NumberInput(attrs={'class': 'form-control'}),
            'Venue': forms.Select(attrs={'class': 'form-control'}),
            'Judge': forms.Select(attrs={'class': 'form-control'}),
            'SpecialGuest': forms.Select(attrs={'class': 'form-control'}),
        }


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ['Name', 'PhoneNo', 'MailId', 'RegNo']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'PhoneNo': forms.NumberInput(attrs={'class': 'form-control'}),
            'MailId': forms.EmailInput(attrs={'class': 'form-control'}),
            'RegNo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SPForm(ModelForm):
    class Meta:
        model = SpecialGuest
        fields = ['Name', 'PhoneNo', 'MailId']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'PhoneNo': forms.NumberInput(attrs={'class': 'form-control'}),
            'MailId': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UpdateWinner(ModelForm):
    def __init__(self, *args, **kwargs):
        e = kwargs.pop('e', None)
        super(UpdateWinner, self).__init__(*args, **kwargs)
        if e is not None:
            self.fields['Winner'] = forms.ModelChoiceField(queryset=e,
                                                           widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['Name', 'Winner']
        widgets = {
            'Name': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }


class CoordinatorForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       validators=[MinLengthValidator(8)])
    field_order = ['Name', 'MailId', 'RegNo', 'Password', 'confirm_password']

    class Meta:
        model = Coordinator
        fields = ['Name', 'RegNo', 'Password', 'PhoneNo', 'MailId']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'PhoneNo': forms.NumberInput(attrs={'class': 'form-control'}),
            'MailId': forms.EmailInput(attrs={'class': 'form-control'}),
            'RegNo': forms.TextInput(attrs={'class': 'form-control'}),
            'Password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(CoordinatorForm, self).clean()
        password = cleaned_data.get("Password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Entered passwords does not match"
            )

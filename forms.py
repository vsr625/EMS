from django import forms
from .models import Participant
from django.forms import ModelForm


class RegisterParticipant(ModelForm):

    class Meta:
        model = Participant
        fields = ['Name', 'Password', 'City', 'PhoneNo', 'College', 'MailId', 'RegNo']
        widgets = {
            'Password': forms.PasswordInput(),
        }
        help_texts = {
            'Name': 'Name of the Participant'
        }


class Login(forms.Form):
    username = forms.CharField(label="Enter Mail ID")
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput())



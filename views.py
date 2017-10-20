from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

# Create your views here.
from EMS.models import Participant, EventParticipates, Event
from .forms import RegisterParticipant, Login


def homepage_view(request):
    pass


def register_view(request):
    if request.method == "POST":
        form = RegisterParticipant(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['MailId'], email=form.cleaned_data['MailId'],
                                            password=form.cleaned_data['Password'])
            user.profile.type = 'p'
            form.save()
            user.save()
            return render(request, 'EMS/register.html', {'registered': True})
    else:
        form = RegisterParticipant()
    return render(request, 'EMS/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                return render(request, 'EMS/login.html', {'form': form, 'error': 'Incorrect Username and password'})
        else:
            return render(request, 'EMS/login.html', {'form': form, 'error': 'Invalid Data Entered'})
    else:
        form = Login()
    return render(request, 'EMS/login.html', {'form': form})


@login_required(login_url='/login')
def logout_view(request):
    form = Login()
    logout(request=request)
    return render(request, 'EMS/login.html', {'form': form, 'error': 'Logged Out successfully'})


@login_required(login_url='/login')
def dashboard_view(request):
    if request.user.profile.type == 'p':
        user = Participant.objects.get(MailId=request.user.username)
        user_id = user.ID
        registered_events_ids = EventParticipates.objects.all().filter(Participant=user_id)
        un_registered_ids_list = [e.Event.EventId for e in registered_events_ids]
        unregistered_events_ids = Event.objects.exclude(EventId__in=un_registered_ids_list)
        registered = Event.objects.filter(EventId__in=registered_events_ids)
        unregistered = Event.objects.filter(EventId__in=unregistered_events_ids)
        return render(request, 'EMS/dashboard.html', {'registered': registered, 'exclude': unregistered})
    else:
        pass


from datetime import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from EMS.models import Participant, EventParticipates, Event, EventCoordinates, Coordinator
from .forms import RegisterParticipant, Login, EventForm, FacultyForm, SPForm, UpdateWinner, CoordinatorForm


def homepage_view(request):
    return render(request, 'EMS/homepage.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterParticipant(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'EMS/register.html', {'success': True})
    else:
        form = RegisterParticipant()
    return render(request, 'EMS/register.html', {'form': form})


def login_p_view(request):
    error = None
    message = request.session.get('message')
    request.session['message'] = None
    if request.method == "POST":
        form = Login(request.POST or None)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.profile.type == 'p':
                login(request, user)
                return redirect('dashboard_p')
            else:
                error = 'Incorrect Username and password'
        else:
            error = 'Invalid Data Entered'
    else:
        form = Login()
    return render(request, 'EMS/login.html', {'form': form, 'error': error, 'user': 'Participant', 'message': message})


def login_c_view(request):
    message = request.session.get('message')
    request.session['message'] = None
    error = None
    if request.method == "POST":
        form = Login(request.POST or None)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.profile.type == 'c':
                login(request, user)
                return redirect('dashboard_c')
            else:
                error = 'Incorrect Username and password'
        else:
            error = 'Invalid Data Entered'
    else:
        form = Login()
    return render(request, 'EMS/login.html', {'form': form, 'error': error, 'user': 'Coordinator', 'message': message})


@login_required(login_url='home')
def logout_view(request):
    profile = request.user.profile.type
    logout(request=request)
    request.session['message'] = 'Successfully logged out'
    if profile == 'c':
        return redirect('login_c')
    elif profile == 'p':
        return redirect('login_p')
    else:
        return redirect('login_a')


@login_required(login_url='/login_p')
def dashboard_p_view(request):
    if request.user.profile.type == 'p':
        message = request.session.get('message')
        request.session['message'] = None
        user = Participant.objects.get(MailId=request.user.username)
        user_name = user.Name
        registered_event_ids = EventParticipates.objects.filter(Participant=user).values_list('Event', flat=True)
        registered = Event.objects.filter(EventId__in=registered_event_ids)
        unregistered = Event.objects.exclude(EventId__in=registered_event_ids).filter(
            Date__gt=datetime.date(datetime.now()))
        return render(request, 'EMS/dashboard_p.html', {'include': registered, 'exclude': unregistered,
                                                        'name': user_name, 'message': message})
    else:
        return redirect('dashboard_c')


@login_required(login_url='/login_c')
def dashboard_c_view(request):
    if request.user.profile.type == 'c':
        message = request.session.get('message')
        request.session['message'] = None
        coordinator = Coordinator.objects.get(MailId=request.user.username)
        date_now = datetime.date(datetime.now())
        eventcoordinator = EventCoordinates.objects.filter(Coordinator=coordinator).values_list('Event', flat=True)
        past_events = Event.objects.filter(EventId__in=eventcoordinator).filter(Date__lt=date_now)
        upcoming_events = Event.objects.filter(EventId__in=eventcoordinator).filter(Date__gte=date_now)
        return render(request, 'EMS/dashboard_c.html',
                      {'past_events': past_events, 'upcoming_events': upcoming_events, 'message': message})
    else:
        return redirect('dashboard_p')


@login_required(login_url='/login_p')
def register_event_view(request, event_id):
    if request.user.profile.type == 'p':
        event = Event.objects.get(EventId=event_id)
        participant = Participant.objects.get(MailId=request.user.username)
        if event is not None and participant is not None:
            new_registration = EventParticipates(Event=event,
                                                 Participant=participant)
            request.session['message'] = 'Succesfully registered to event ' + event.Name
            new_registration.save()
        return redirect('dashboard_p')
    else:
        return redirect('dashboard_c')


@login_required(login_url='/login_a')
def create_event_view(request):
    if request.user.profile.type == 'a':
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                coordinator = form.cleaned_data['Coordinator']
                form.save()
                for c in coordinator:
                    new_event_coordinator = EventCoordinates(Event=Event.objects.get(Name=form.cleaned_data['Name']),
                                                             Coordinator=c)
                    new_event_coordinator.save()
                request.session['message'] = 'Successfully created ' + form.cleaned_data['Name']
                return redirect('dashboard_a')
        else:
            form = EventForm()
        return render(request, 'EMS/form_template.html', {'form': form, 'heading': 'Create New Event'})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def create_faculty_view(request):
    if request.user.profile.type == 'a':
        if request.method == 'POST':
            form = FacultyForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['message'] = 'Successfully created ' + form.cleaned_data['Name']
                return redirect('dashboard_a')
        else:
            form = FacultyForm()
        return render(request, 'EMS/form_template.html', {'form': form, 'heading': 'Create New Faculty'})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def create_sp_view(request):
    if request.user.profile.type == 'a':
        if request.method == 'POST':
            form = SPForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['message'] = 'Successfully created ' + form.cleaned_data['Name']
                return redirect('dashboard_a')
        else:
            form = SPForm()
        return render(request, 'EMS/form_template.html', {'form': form, 'heading': 'Create New Special Guest'})
    else:
        return redirect('home')


@login_required(login_url='/login_c')
def update_winner(request, event_id):
    if request.user.profile.type == 'c':
        if request.method == 'POST':
            form = UpdateWinner(request.POST, instance=Event.objects.get(EventId=event_id))
            if form.is_valid():
                form.save()
                request.session['message'] = 'Succesfully updated event ' + form.cleaned_data['Name']
                return redirect('dashboard_c')
        else:
            if not EventCoordinates.objects.filter(Coordinator=Coordinator.objects.get(MailId=request.user.username),
                                                   Event=Event.objects.get(EventId=event_id)):
                request.session['message'] = 'Unauthorized Access'
                return redirect('dashboard_c')
            event = Event.objects.get(EventId=event_id)
            participant_id_list = EventParticipates.objects.filter(Event=event).values_list('Participant', flat=True)
            participant_list = Participant.objects.filter(ID__in=participant_id_list)
            form = UpdateWinner(instance=event, e=participant_list)
            return render(request, 'EMS/update_winner.html', {'form': form})
    else:
        return redirect('dashboard_p')


def login_a_view(request):
    message = request.session.get('message')
    request.session['message'] = None
    error = None
    if request.method == "POST":
        form = Login(request.POST or None)
        if form.is_valid():
            user = authenticate(username='admin',
                                password=form.cleaned_data['password'])
            if user is not None and user.profile.type == 'a':
                login(request, user)
                return redirect('dashboard_a')
            else:
                error = 'Incorrect Username and password'
        else:
            error = 'Invalid Data Entered'
    else:
        form = Login()
    return render(request, 'EMS/login.html', {'form': form, 'error': error, 'user': 'Admin', 'message': message})


@login_required(login_url='/login_a')
def update_event(request, event_id):
    if request.user.profile.type == 'a':
        if request.method == 'POST':
            form = EventForm(request.POST, instance=Event.objects.get(EventId=event_id))
            if form.is_valid():
                form.save()
                event = Event.objects.get(Name=form.cleaned_data['Name'])
                EventCoordinates.objects.filter(Event=event).delete()
                coordinator = form.cleaned_data['Coordinator']
                for c in coordinator:
                    eventcor = EventCoordinates(Event=Event.objects.get(Name=form.cleaned_data['Name']), Coordinator=c)
                    eventcor.save()
                request.session['message'] = 'Successfully updated event ' + form.cleaned_data['Name']
                return redirect('dashboard_a')
        else:
            event_cor = EventCoordinates.objects.filter(Event=Event.objects.get(EventId=event_id))
            form = EventForm(instance=Event.objects.get(EventId=event_id),
                             initial={'Coordinator': event_cor.values_list('Coordinator', flat=True)})
        return render(request, 'EMS/form_template.html', {'form': form, 'heading': 'Update Event'})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def delete_event(request, event_id):
    if request.user.profile.type == 'a':
        if request.method == 'POST':
            name = Event.objects.get(EventId=event_id).Name
            Event.objects.get(EventId=event_id).delete()
            request.session['message'] = 'Successfully deleted event ' + name
            return redirect('dashboard_a')
        else:
            return render(request, 'EMS/delete_event.html', {
                'heading': 'Are you sure you want to delete the event ' + Event.objects.get(
                    EventId=event_id).Name + '?'})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def dashboard_a_view(request):
    message = request.session.get('message')
    request.session['message'] = None
    if request.user.profile.type == 'a':
        events = Event.objects.all()
        return render(request, 'EMS/dashboard_a.html', {'name': 'Admin', 'events': events, 'message': message})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def create_co_view(request):
    if request.user.profile.type == 'a':
        if request.method == "POST":
            form = CoordinatorForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['message'] = 'Successfully created ' + form.cleaned_data['Name']
                return redirect('dashboard_a')
        else:
            form = CoordinatorForm()
        return render(request, 'EMS/form_template.html', {'form': form, 'heading': 'Create New Coordinator'})
    else:
        return redirect('home')


@login_required(login_url='/login_a')
def view_event(request, event_id):
    if request.user.profile.type == 'a':
        event = Event.objects.get(EventId=event_id)
        coord = EventCoordinates.objects.filter(Event=event)
        participants_ids = EventParticipates.objects.filter(Event=event).values_list('Participant', flat=True)
        participants = Participant.objects.filter(ID__in=participants_ids)
        return render(request, 'EMS/view_event.html',
                      {'event': event, 'participants': participants, 'coord': coord, 'type': request.user.profile.type})
    elif request.user.profile.type == 'c':
        if not EventCoordinates.objects.filter(Coordinator=Coordinator.objects.get(MailId=request.user.username),
                                               Event=Event.objects.get(EventId=event_id)):
            request.session['message'] = 'Unauthorized Access'
            return redirect('dashboard_c')
        event = Event.objects.get(EventId=event_id)
        coord = EventCoordinates.objects.filter(Event=event)
        participants_ids = EventParticipates.objects.filter(Event=event).values_list('Participant', flat=True)
        participants = Participant.objects.filter(ID__in=participants_ids)
        return render(request, 'EMS/view_event.html',
                      {'event': event, 'participants': participants, 'coord': coord,
                       'type': request.user.profile.type})
    else:
        return redirect('home')


# todo implement this
def generate_view(request):
    return None

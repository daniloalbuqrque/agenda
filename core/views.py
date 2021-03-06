from django.shortcuts import render, redirect
from core.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

#def index(request):
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid user or password. Try again!")
            return redirect('/')

@login_required(login_url='/login/')
def events_list(request):
    user = request.user
    event = Event.objects.filter(user=user)
    data = {'events':event}
    return render(request, 'agenda.html', data)

@login_required(login_url='/login/')
def event(request):
    id_event = request.GET.get('id')
    data = {}
    if id_event:
        data['event'] = Event.objects.get(id=id_event)
    return render(request, 'event.html', data)

@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        user = request.user
        id_event = request.POST.get('id_event')
        if id_event:
            Event.objects.filter(id=id_event).update(title=title,
                                                     event_date=event_date,
                                                     description=description)
        else:
            Event.objects.create(title=title,
                                 event_date=event_date,
                                 description=description,
                                 user=user)
    return redirect('/')

@login_required(login_url='/login/')
def delete_event(request, id_event):
    user = request.user
    event = Event.objects.get(id=id_event)
    if user == event.user:
        event.delete()
    return redirect('/')
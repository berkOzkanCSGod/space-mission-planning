from django.shortcuts import render
from django.http import HttpResponse
from .models import Astronaut, Company, Space_Mission
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import connection
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse

import random

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        email = request.POST['email-input']
        password = request.POST['password-input']

        role = Astronaut.findRole(email)

        if role == 'astronaut':
            user = Astronaut.authenticateUser(email, password)
            if user is not None:
                response = HttpResponseRedirect(reverse('home'))
                response.set_cookie('user_id', user.astro_id)
                response.set_cookie('user_role', role)
                return response
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'err_msg': error_message})
        elif role == 'company':
            user = Company.authenticateUser(email, password)
            if user is not None:
                response = HttpResponseRedirect(reverse('home'))
                response.set_cookie('user_id', user.c_id)
                response.set_cookie('user_role', role)
                return response
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'err_msg': error_message})

        else:
            error_message = 'Email does not exists in our database'
            return render(request, 'login.html', {'err_msg': error_message})

        
    else:
        return render(request, "login.html")

def signup(request):
    if (request.method == 'POST'):
        email = request.POST['email-input']
        password = request.POST['password-input']
        role = request.POST['role']
        print("Role:  ", role)
        if role == 'astronaut':
            user = Astronaut.createAstro(email, password)
            
            if user is not None:
                response = HttpResponseRedirect(reverse('home'))
                response.set_cookie('user_id', user.astro_id)
                response.set_cookie('user_role', 'astronaut')
                return response
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'signup.html', {'err_msg': error_message})
        elif role == 'company':
            user = Company.createComp(email, password)
            
            if user is not None:
                response = HttpResponseRedirect(reverse('home'))
                response.set_cookie('user_id', user.c_id)
                response.set_cookie('user_role', 'company')
                return response
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'signup.html', {'err_msg': error_message})
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'signup.html', {'err_msg': error_message})


    else:
        return render(request, "signup.html")
    
def logout(request):
    if 'user_id' in request.COOKIES:
        response = HttpResponseRedirect(reverse('login'))
        response.delete_cookie('user_id')
        response.delete_cookie('user_role')
        return response
    else:
        return HttpResponseRedirect(reverse('login'))
    
def home(request):
    if 'user_id' not in request.COOKIES:
        response = HttpResponseRedirect(reverse('login'))
        return response
    else:
        user_id = request.COOKIES.get('user_id')
        user_role = request.COOKIES.get('user_role')
        
        if user_id:
            return render(request, "home.html")
        else:
            error_message = 'You need to log in to access this page.'
            return HttpResponseRedirect(reverse('login'), {'err_msg': error_message})

def profile(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        response = HttpResponseRedirect(reverse('login'))
        return response
    if user_role == 'astronaut':
        user = Astronaut.getUserById(user_id)
        if user:
            return render(request, "profile.html", {'profile': user, 'role': user_role})
    elif user_role == 'company':
        user = Company.getUserById(user_id)
        if user:
            return render(request, "profile.html", {'profile': user, 'role': user_role})

    error_message = 'Issue with accessing profile'
    return HttpResponseRedirect(reverse('home')) 

def update_field(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        response = HttpResponseRedirect(reverse('login'))
        return response
    field = request.GET.get('field')
    input = request.POST.get('input')

    print("Field:", field)
    print("input:", input)
    print("role:", user_role)

    if user_role == 'astronaut':
        Astronaut.updateAttribute(user_id, field, input)
        return HttpResponseRedirect(reverse('profile')) 
    elif user_role == 'company':
        Company.updateAttribute(user_id, field, input)
        return HttpResponseRedirect(reverse('profile')) 

def dashboard(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    
    if (request.method == 'POST'):
        pass
    else:
        return render(request, "dashboard.html")
    
def create_mission(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role == 'astronaut':
        return HttpResponseRedirect(reverse('home'))

    if (request.method == 'POST'):
        name = request.POST.get('sm_name-input')
        destination = request.POST.get('sm_destination-input')
        duration = request.POST.get('sm_duration-input')
        astronaut_count = request.POST.get('sm_astro_cnt-input')
        objective = request.POST.get('sm_objective-input')
        launch_site = request.POST.get('sites')
        launch_date = request.POST.get('date-input')
        ls = Space_Mission.getLaunchSites()

        res = Space_Mission.createMission(user_id, name, destination, duration, astronaut_count, objective, launch_site, launch_date)

        if res is not None:
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "create_mission.html", {'err_msg': 'Could not create mission', 'launch_sites': ls})


    else:
        ls = Space_Mission.getLaunchSites()
        return render(request, "create_mission.html", {'launch_sites': ls})
    

def space_missions(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    
    if (request.method == 'POST'):
        filter = request.POST.get('filter')
        missions = Space_Mission.filter(filter)

        return render(request, "space_missions.html", {'missions': missions, 'filter': filter})

    else:
        return render(request, "space_missions.html", {'missions': Space_Mission.getAllMissions()})
    
def place_bid(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role == 'astronaut':
        return HttpResponseRedirect(reverse('home'))
    
    #additional checks

    mission_name = request.GET.get('mission_name')

    if (request.method == 'POST'):
        amount = request.POST.get('bid_amount')
        sm_id = request.POST.get('mission_id')
        print("dddddddddddddddddddddddddddddd:",sm_id)
        res = Space_Mission.placeBid(sm_id, user_id, amount)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "place_bid.html", {'mission': Space_Mission.getMissionByName(mission_name)})
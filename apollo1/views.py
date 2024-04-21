from django.shortcuts import render
from django.http import HttpResponse
from .models import Astronaut, Company
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


def update_field():
    pass

# def profile(request):
#     user_id = request.session.get('user_id')
#     user_role = request.session.get('user_role')

#     if user_id:
#         user = Users.getUserById(user_id, user_role)
#         if user:
#             return render(request, "profile.html", {'profile': user})

#     return None

# def update_field(request):
#     if request.method == "POST":
#         field_name = request.POST.get("field")
#         input_value = request.POST.get("input_value") 
#         user_id = request.session.get('user_id')
#         user_role = request.session.get('user_role')
        
#         update = Users.updateAttribute(user_id, user_role, field_name, input_value)

#         if update is None:
#             return HttpResponseRedirect(reverse('profile'))
#         else:
#             return render(request, 'profile.html', {'error_message': update})
#     else:
#         return HttpResponse("Invalid request method.")
from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import connection
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = Users.authenticateUser(username, password)

        if user is not None:
                request.session['user_id'] = user.uid
                request.session['user_role'] = Users.findUserRole(user.uid)

                print("Logged in!")
                return HttpResponseRedirect(reverse('home'))
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})

    else:
        if 'login_success' in request.session:
            del request.session['login_success']

        return render(request, "login.html")

def signup(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        role = request.POST['role']

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
        
        user = Users.createUser(username, email, password, role)

        if user != None:
            request.session['user_id'] = user.uid
            request.session['user_role'] = role
            print("Logged in!")
            return HttpResponseRedirect(reverse('home'))
        else:
            error_message = 'Invalid username or password.'
            return render(request, 'signup.html', {'error_message': error_message})

    else:
        if 'login_success' in request.session:
            del request.session['login_success']

        return render(request, "signup.html")
    
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return HttpResponseRedirect(reverse('login'))
    
def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        return render(request, "home.html", {'users': user_id})
    else:
        error_message = 'You need to log in to access this page.'
        return HttpResponseRedirect(reverse('login'))

def profile(request):
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if user_id:
        user = Users.getUserById(user_id, user_role)
        if user:
            return render(request, "profile.html", {'profile': user})

    return None

def update_field(request):
    if request.method == "POST":
        field_name = request.POST.get("field")
        input_value = request.POST.get("input_value") 
        user_id = request.session.get('user_id')
        user_role = request.session.get('user_role')
        
        update = Users.updateAttribute(user_id, user_role, field_name, input_value)

        if update is None:
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'profile.html', {'error_message': update})
    else:
        return HttpResponse("Invalid request method.")
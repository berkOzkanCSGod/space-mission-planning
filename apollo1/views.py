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
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

@api_view(['GET']) #THIS IS FOR HANDLING THE API REQUESTS COMING FROM REACT
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = Users.authenticateUser(username, password)
        if user != None:
                request.session['user_id'] = user.id
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
        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
        user = Users.createUser(username, password)
        if user != None:
            request.session['user_id'] = user.id
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
        user = Users.objects.get(id=user_id)
        users = Users.getAllUsers()
        return render(request, "home.html", {'users': users})
    else:
        error_message = 'You need to log in to access this page.'
        return HttpResponseRedirect(reverse('login'))

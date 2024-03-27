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
import json
import random

@api_view(['GET']) #THIS IS FOR HANDLING THE API REQUESTS COMING FROM REACT
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = Users.authenticateUser(username, password)
        if user is not None:
            request.session['user_id'] = user.id
            print("Logged in!")
            return Response({'message': 'Logged in!'})
        else:
            return Response({'error_message': 'Invalid username or password.'})
        
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        userType = data.get('userType')
        if Users.checkUserExists(username):
            print("User already exists.")
            return Response({'error_message': 'User already exists.'})
    
        if userType == 'Admin':
            user = Users.createUser(username, password)
        elif userType == 'Company':
            country = data.get('country')
            valuation = data.get('valuation')
            numberOfEmployees = data.get('numberOfEmployees')
            budget = data.get('budget')
            user = Users.createUser(username, password)
        elif userType == 'Astronaut':
            nationality = data.get('nationality')
            age = data.get('age')
            education = data.get('education')
            height = data.get('height')
            weight = data.get('weight')
            vocation = data.get('vocation')
            securityClearance = data.get('securityClearance')
            user = Users.createUser(username, password)
        
        if user != None:
            request.session['user_id'] = user.id
            print("Logged in!")
            return Response({'message': 'Logged in!'})
        else:
            return Response({'error_message': 'Invalid username or password.'})
    
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

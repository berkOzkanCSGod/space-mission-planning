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
    
def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
        users = Users.getAllUsers()
        return render(request, "home.html", {'users': users})
    else:
        error_message = 'You need to log in to access this page.'
        return HttpResponseRedirect(reverse('login'))

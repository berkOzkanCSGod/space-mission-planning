from django.shortcuts import render
from django.http import HttpResponse
from .models import allUsers, User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def home(request):
    users = allUsers.objects.all()
    return render(request, "home.html", {'users':users})

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)

        # Check if username and password match a record in the database
        if User.objects.filter(username=username, password=password).exists():
            # Authentication successful, redirect to a success page
            return HttpResponseRedirect(reverse('home'))
        else:
            # Authentication failed, display an error message
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})

    else:
        return render(request, "login.html")
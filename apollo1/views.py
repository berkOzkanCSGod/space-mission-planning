from django.shortcuts import render
from django.http import HttpResponse
from .models import Astronaut, Company, Space_Mission, Bank_Account, Transaction, Admin
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
    if request.method == 'POST':
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
            user = Admin.authenticateUser(email, password)
            if user is not None:
                response = HttpResponseRedirect(reverse('home'))
                response.set_cookie('user_id', user.admin_id)
                response.set_cookie('user_role', role)
                return response
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'err_msg': error_message})

        
    else:
        return render(request, "login.html")


def signup(request):
    if request.method == 'POST':
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
        elif role == 'organization':
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
            return render(request, "home.html", {'user_id': user_id, 'user_role': user_role})
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
    elif user_role == 'admin':
        user = Admin.getUserById(user_id)
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
    
    if request.method == 'POST':
        pass
    else:
        return render(request, "dashboard.html", {'user_id': user_id, 'user_role': user_role})


def create_mission(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role == 'astronaut':
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
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


def system_report(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    report_type = request.GET.get('report_type')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    if user_role != 'admin':
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'GET':
        if report_type == 'most_expensive_mission':
            return render(request, "system_report.html", {'missions': Space_Mission.getMostExpensiveMission(), 'report_type': report_type})
        elif report_type == 'mission_with_most_astronauts':
            return render(request, "system_report.html", {'missions': Space_Mission.getMissionWithMostAstronauts(), 'report_type': report_type})
        elif report_type == 'most_active_creator_company':
            return render(request, "system_report.html", {'companies': Company.getMostActiveCreatorCompany(), 'report_type': report_type})
        elif report_type == 'most_active_executor_company':
            return render(request, "system_report.html", {'companies': Company.getMostActiveExecutorCompany(), 'report_type': report_type})
        elif report_type == 'mission_with_highest_bid':
            return render(request, "system_report.html", {'missions': Space_Mission.getMissionWithHighestBid(), 'report_type': report_type})
        else:
            return HttpResponseRedirect(reverse('home'))


def space_missions(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'POST':
        filter = request.POST.get('filter')
        order_field = request.POST.get('orderField')
        order_direction = request.POST.get('orderDirection')
        missions = Space_Mission.filter(filter, order_field, order_direction)

        return render(request, "space_missions.html", {'missions': missions, 'filter': filter})

    else:
        return render(request, "space_missions.html", {'missions': Space_Mission.getAllMissions()})


def space_mission(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    mission_name = None
    if request.method == 'GET':
        mission_name = request.GET.get('mission_name')
    elif request.method == 'POST':
        mission_name = request.POST.get('mission_name')
        c_id = request.POST.get('company_id')
        mission = Space_Mission.getMissionByName(mission_name)
        sm_id = Space_Mission.findIdByName(mission_name)
        if c_id:
            # check if the company is the creator of the mission
            if int(c_id) == int(user_id):
                return HttpResponseRedirect(reverse('home'))
            Space_Mission.acceptBid(sm_id, c_id, user_id)
        status = request.POST.get('status')
        if status:
            Space_Mission.updateStatus(sm_id, status)

    mission = Space_Mission.getMissionByName(mission_name)
    sm_id = Space_Mission.findIdByName(mission_name)
    bids = list(Space_Mission.findBids(sm_id))
    sm_trainings = Space_Mission.getRequiredTrainings(sm_id)
    for i in range(0, len(bids)):
        bids[i] = list(bids[i])
        bids[i].append(Company.getUserById(bids[i][1]).c_name)
        print(bids[i])
    print(bids)
    performs_mission = Space_Mission.findPerformingMission(sm_id)
    print('performs', performs_mission)
    performer = None
    if performs_mission:
        performer = Company.getUserById(performs_mission[0])
    print('performer', performer)
    creator_id = Space_Mission.findCreatorId(sm_id)
    creator = Company.getUserById(creator_id)
    is_creator = int(creator_id) == int(user_id)
    is_performer = False
    if performs_mission:
        is_performer = int(performer.c_id) == int(user_id)
    company_astros = []
    if is_performer:
        company_astros = list(Company.getTrainedAstronauts(sm_id, user_id))
    assigned_astros = list(Space_Mission.getAssignedAstronauts(sm_id))
    print(sm_id)
    print(creator_id)
    print(user_id)
    print(is_creator)
    print(is_performer)

    return render(request, "space_mission.html", {'mission': mission, 'bids': bids, 'performs_mission': performs_mission, "performer":performer, "is_creator": is_creator, "is_performer": is_performer, "creator":creator, "sm_trainings": sm_trainings, "company_astros": company_astros, "assigned_astros": assigned_astros})


def place_bid(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role == 'astronaut':
        return HttpResponseRedirect(reverse('home'))
    
    # additional checks

    mission_name = request.GET.get('mission_name')

    if request.method == 'POST':
        amount = request.POST.get('bid_amount')
        sm_id = request.POST.get('mission_id')
        res = Space_Mission.placeBid(sm_id, user_id, amount)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "place_bid.html", {'mission': Space_Mission.getMissionByName(mission_name)})
    

def assign_astro(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role != 'company':
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        mission_name = request.POST.get('mission_name')
        astro_id = request.POST.get('astro_id')
        print(mission_name, astro_id)
        sm_id = Space_Mission.findIdByName(mission_name)
        print(sm_id)
        res = Space_Mission.assignAstro(sm_id, astro_id)
    return HttpResponseRedirect(reverse('dashboard'))

def fire_astro(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    elif user_role != 'company':
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        mission_name = request.POST.get('mission_name')
        astro_id = request.POST.get('astro_id')
        sm_id = Space_Mission.findIdByName(mission_name)
        res = Space_Mission.fireAstro(sm_id, astro_id)
    return HttpResponseRedirect(reverse('dashboard'))



def user_missions(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role') 
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    
    if user_role == 'company':
        created_missions = Company.getCreatedMissions(user_id)
        performing_missions = Company.getPerformingMissions(user_id)
    elif user_role == 'astronaut':
        performing_missions = Astronaut.getPerformingMissions(user_id)
        pass

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home'))
    else:
        if user_role == 'company':
            return render(request, "user_missions.html", {'created_missions': created_missions, 'performing_missions':performing_missions, 'user_role': user_role})
        elif user_role == 'astronaut':
            return render(request, "user_missions.html", {'performing_missions':performing_missions, 'user_role': user_role})
        else:
            return HttpResponseRedirect(reverse('home'))


def training_view(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home'))
    else:
        astro_trainings = Astronaut.getAstronautTrainings(user_id)
        return render(request, "training_view.html", {'astro_trainings': astro_trainings})


def get_bank_account(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    if user_role == 'company':
        bank = Bank_Account.getBankAccount(user_id)
    else:
        pass
    return render(request, "bank_account.html", {'bank': bank})


def create_bank_account(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    if user_role == 'company':
        if request.method == 'POST':
            company_id = user_id
            account_number = request.POST.get('account_number')
            Bank_Account.createBankAccount(company_id, account_number)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "bank_account.html")
    else:
        return HttpResponseRedirect(reverse('home'))


def make_transaction(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    if user_role == 'company':
        if request.method == 'POST':
            # get the bank account numbers and amount
            from_account = request.POST.get('from_account')
            to_account = request.POST.get('to_account')
            amount = float(request.POST.get('amount'))
            success = Transaction.createTransaction(from_account, to_account, amount)
            if success:
                return HttpResponseRedirect(reverse('get_bank_account'))  # redirect to bank account page
            else:
                return render(request, "bank_account.html", {'err_msg': 'Could not make transaction'})
        elif request.method == 'GET':
            # get the bank account of the company
            bank = Bank_Account.getBankAccount(user_id)
            return render(request, "bank_account.html", {'bank': bank})
    else:
        return HttpResponseRedirect(reverse('home'))


def get_all_transactions(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')
    if 'user_id' not in request.COOKIES:
        return HttpResponseRedirect(reverse('login'))
    if user_role == 'company':
        transactions = Transaction.getTransactions(user_id)
        return render(request, "transactions.html", {'transactions': transactions})
    else:
        return HttpResponseRedirect(reverse('home'))


def get_filtered_transactions(request):
    user_id = request.COOKIES.get('user_id')
    user_role = request.COOKIES.get('user_role')

    # Check if user is logged in and has the company role
    if not user_id or user_role != 'company':
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        date = request.POST.get('date')
        amount_less_than = request.POST.get('amount_less_than')
        amount_greater_than = request.POST.get('amount_greater_than')
    else:
        date = None
        amount_less_than = None
        amount_greater_than = None

    # Convert amounts to proper types or set to None if not provided
    amount_less_than = float(amount_less_than) if amount_less_than else None
    amount_greater_than = float(amount_greater_than) if amount_greater_than else 0

    # Retrieve transactions based on filters
    transactions = Transaction.getFilteredTransactions(user_id, date, amount_less_than, amount_greater_than)

    # Render the transactions to the template
    return render(request, "transactions.html", {'transactions': transactions})

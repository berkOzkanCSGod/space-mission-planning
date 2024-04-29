from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#url config module
urlpatterns = [
    path("home/", views.home, name='home'),
    path("home/profile", views.profile, name='profile'),
    path("home/update", views.update_field, name='update_field'),
    path("home/dashboard", views.dashboard, name='dashboard'),
    path("home/create_mission", views.create_mission, name='create_mission'),
    path("home/space_missions", views.space_missions, name='space_missions'),
    path("home/space_mission", views.space_mission, name='space_mission'),
    path("home/space_mission/assign_astro", views.assign_astro, name='assign_astro'),
    path("home/user_missions", views.user_missions, name='user_missions'),
    path("home/place_bid", views.place_bid, name='place_bid'),
    path("home/training_view", views.training_view, name='training_view'),
    path("home/system_report", views.system_report, name='system_report'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
    path("home/bank_account", views.get_bank_account, name='get_bank_account'),
    path("home/create_bank_account", views.create_bank_account, name='create_bank_account'),
    path("home/make_transaction", views.make_transaction, name='make_transaction'),
    path("home/transactions", views.get_filtered_transactions, name='get_filtered_transactions'),
]

# urlpatterns += staticfiles_urlpatterns()
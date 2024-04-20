from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#url config module
urlpatterns = [
    path("home/", views.home, name='home'),
    path("home/profile", views.profile, name='profile'),
    path("home/update", views.update_field, name='update_field'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
]

# urlpatterns += staticfiles_urlpatterns()
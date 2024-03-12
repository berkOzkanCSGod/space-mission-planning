from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#url config module
urlpatterns = [
    path("hello_world/", views.hello_world, name='react-test'),
    path("home/", views.home, name='home'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
]

# urlpatterns += staticfiles_urlpatterns()
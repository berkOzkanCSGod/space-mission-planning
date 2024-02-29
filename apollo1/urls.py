from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#url config module
urlpatterns = [
    path("home/", views.home, name='home'),
    path("login/", views.login, name='login')
]

# urlpatterns += staticfiles_urlpatterns()
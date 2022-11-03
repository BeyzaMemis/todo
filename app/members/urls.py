from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('Home/', views.Home, name='home'),
    path('people/', views.people, name='people'),
]
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render


def Home(request):
    return render(request, 'main/home.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("homee")
            login(request, user)
            return redirect('home')
        else:
            print("loginn")
            return redirect('http://127.0.0.1:8000/Home/')
    else:
        return render(request, 'members/login.html', {})

# Create your views here.

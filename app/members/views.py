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

            login(request, user)
            return redirect('home')
        else:

            return redirect('login_user')
    else:
        return render(request, 'members/login.html', {})


def people(request):
    return render(request, 'members/people.html', {})

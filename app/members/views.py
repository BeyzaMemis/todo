from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render
from core.models import User
from django.core.paginator import Paginator


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
    # for i in range(20):
    #     user_name = 'Test'+str(i)
    #     user_mail = user_name+'@test.com'
    #     password = "test"
    #     User.objects.create_user(user_name,user_mail,password)
    user_list = User.objects.all()
    #pagination

    paginator = Paginator(User.objects.all(), 3)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    nums = "a" * users.paginator.num_pages

    return render(request, 'members/people.html', {'user_list': user_list, 'users': users, 'nums': nums })


def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        pass
    return render(request, 'members/user_detail.html', {'user': user})

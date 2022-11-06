from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render
from core.models import User, UserManager, Projects
from django.core.paginator import Paginator
from .forms import UserForm, ProjectForm
from django.http import HttpResponseRedirect


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
    # pagination

    paginator = Paginator(User.objects.all(), 3)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    nums = "a" * users.paginator.num_pages

    return render(request, 'members/people.html', {'users': users, 'nums': nums})


def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None
    return render(request, 'members/user_detail.html', {'user': user})


def search_user(request):
    empty_list = False
    if request.method == 'POST':
        searched = request.POST.get('searched')
        searched_users = User.objects.filter(username__icontains=searched)
        if len(searched_users) == 0:
            empty_list = True

        return render(request, 'members/user_search.html',
                      {'searched': searched, 'users': searched_users, 'empty_list': empty_list})
    else:
        return render(request, 'members/user_search.html', {})


def add_user(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            User.objects.create_user(data['username'], data['email'], data['password'], data['current_project'])
            return redirect('home')

    return render(request, 'members/add_user.html', {'form': form})


def show_projects(request):
    project_list = Projects.objects.all()
    total_projects = len(project_list)
    # for i in range(20):
    #     name = "Test"+str(i)
    #     Projects.objects.create(name=name, is_active=True)
    paginator = Paginator(project_list, 3)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    nums = "a" * projects.paginator.num_pages

    return render(request, 'members/projects_second.html', {'projects': projects, 'nums': nums, 'total_projects': total_projects})


def project_detail(request, project_id):
    try:
        project = Projects.objects.get(id=project_id)
    except:
        project = None
    return render(request, 'members/project_detail.html', {'project': project})


def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print("form burda")
        if form.is_valid():
            print("form valid")
            form.save()
            return redirect('show_projects')

    return render(request, 'members/create_project.html', {'form': form})


def update_project(request, pk):
    project = Projects.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('show_projects')


    return render(request, 'members/create_project.html', {'form': form})

def delete_project(request, pk):
    project = Projects.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('show_projects')
    return render(request, 'members/delete_project.html', {'project': project})


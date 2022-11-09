from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from core.models import User, UserManager, Projects
from django.core.paginator import Paginator
from .forms import UserForm, ProjectForm, UserUpdateForm
from .filters import ProjectFilter
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


class People(View):
    def get(self, request):
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

        return render(request, 'members/people_second.html', {'users': users, 'nums': nums})


def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None
    return render(request, 'members/user_detail.html', {'user': user})


class SearchUser(View):

    def post(self, request):
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


class AddUser(View):

    def post(self, request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                User.objects.create_user(data['username'], data['email'], data['password'], )
                return redirect('home')

    def get(self, request):
        projects = Projects.objects.all()
        form = UserForm()
        return render(request, 'members/add_user.html', {'form': form, 'projects': projects})


class ShowProjects(View):

    def get(self, request):
        project_list = Projects.objects.all()
        total_projects = len(project_list)
        project_filter = ProjectFilter(request.GET, queryset=project_list)
        project_list = project_filter.qs
        print(project_filter.data)
        # for i in range(20):
        #     name = "Test"+str(i)
        #     Projects.objects.create(name=name,description="deneme", is_active=True)
        paginator = Paginator(project_list, 3)
        page = request.GET.get('page')
        projects = paginator.get_page(page)
        nums = "a" * projects.paginator.num_pages

        return render(request, 'members/projects_second.html',
                      {'projects': projects, 'nums': nums, 'total_projects': total_projects,
                       'project_filter': project_filter, 'criteria': project_filter.data})


def project_detail(request, project_id):
    try:
        project = Projects.objects.get(id=project_id)
    except:
        project = None
    return render(request, 'members/project_detail.html', {'project': project})


class CreateProject(View):

    def post(self, request):
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            print("form burda")
            if form.is_valid():
                print("form valid")
                form.save()
                return redirect('show_projects')

    def get(self, request):
        form = ProjectForm()
        return render(request, 'members/create_project_old.html', {'form': form})


class UpdateProject(View):
    def post(self, request, pk):
        project = Projects.objects.get(id=pk)
        form = request.POST
        Projects.objects.filter(id=pk).update(name=form.get('name'), description=form.get('description'),
                                              active_issue_count=form.get('active_issue_count'),
                                              solved_issue_count=form.get('solved_issue_count'),
                                              start_date=form.get('start_date'), deadline=form.get('deadline'))

        return redirect('show_projects')

    def get(self, request, pk):
        project = Projects.objects.get(id=pk)
        form = ProjectForm(instance=project)

        return render(request, 'members/create_project_old.html', {'form': form})


class DeleteProject(View):

    def post(self, request, pk):
        project = Projects.objects.get(id=pk)
        if request.method == 'POST':
            user = User.objects.get(current_project_id=project.id)
            if user:
                User.objects.filter(id=user.id).update(current_project_id=None)

            project.delete()
            return redirect('show_projects')

    def get(self, request, pk):
        project = Projects.objects.get(id=pk)
        return render(request, 'members/delete_project.html', {'project': project})


class UpdateUser(View):
    def post(self, request, pk):

        user = User.objects.get(id=pk)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('people')
        else:
            # formu kaydet
            return redirect('members/update_user.html', {'form': form})

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = UserUpdateForm(instance=user)
        return render(request, 'members/update_user.html', {'form': form})


class DeleteUser(View):

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()

        return redirect('people')

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, 'members/delete_user.html', {'user': user})


class AssignProjectToUser(View):

    def post(self, request, pk):
        User.objects.filter(id=pk).update(current_project=request.POST.get('project'))

        return redirect('people')

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        projects = Projects.objects.all()
        return render(request, 'members/assign_project_to_user.html', {'user': user, 'projects': projects})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from core.models import User, UserManager, Project, UserProjectRelation, Issue
from django.core.paginator import Paginator
from .forms import UserForm, ProjectForm, UserUpdateForm, IssuesForm
from .filters import ProjectFilter
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def get_user_current_projects(user_id):
    projects = UserProjectRelation.objects.filter(user__id=user_id).values('project')
    project_names = []
    for project in projects:
        project_names.append(Project.objects.get(id=project.get('project')).name)

    return ', '.join(project_names)


def check_user_project_relation_exist(user_id, project_id):
    relations = UserProjectRelation.objects.filter(user__id=user_id)
    for relation in relations:
        if relation.project.id == project_id:
            return True
    return False


@login_required(login_url="login_user")
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
            messages.info(request, "User name OR password is not correct !")
            return redirect('login_user')
    else:
        return render(request, 'members/login.html', {})


def log_out_user(request):
    logout(request)
    return redirect('login_user')


class People(LoginRequiredMixin, View):
    login_url = 'login_user'

    def get(self, request):
        # for i in range(20):
        #     user_name = 'Test'+str(i)
        #     user_mail = user_name+'@test.com'
        #     password = "test"
        #     User.objects.create_user(user_name,user_mail,password)

        paginator = Paginator(User.objects.all(), 3)
        page = request.GET.get('page')
        users = paginator.get_page(page)
        nums = ["page"] * users.paginator.num_pages

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
        searched = request.POST.get('searched')
        searched_users = User.objects.filter(username__icontains=searched)
        if len(searched_users) == 0:
            empty_list = True

        return render(request, 'members/user_search.html',
                      {'searched': searched, 'users': searched_users, 'empty_list': empty_list})

    def get(self, request):
        return render(request, 'members/user_search.html', {})


class AddUser(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            User.objects.create_user(data['username'], data['email'], data['password'], )
            return redirect('home')

    def get(self, request):
        projects = Project.objects.all()
        form = UserForm()
        return render(request, 'members/add_user.html', {'form': form, 'projects': projects})


class ShowProjects(LoginRequiredMixin, View):
    login_url = 'login_user'

    def get(self, request):
        project_list = Project.objects.all()
        total_projects = len(project_list)
        project_filter = ProjectFilter(request.GET, queryset=project_list)
        project_list = project_filter.qs
        # for i in range(20):
        #     name = "Test"+str(i)
        #     Projects.objects.create(name=name,description="deneme", is_active=True)
        paginator = Paginator(project_list, 3)
        page = request.GET.get('page')
        projects = paginator.get_page(page)
        nums = ["page"] * projects.paginator.num_pages

        return render(request, 'members/projects_second.html',
                      {'projects': projects, 'nums': nums, 'total_projects': total_projects,
                       'project_filter': project_filter, 'criteria': project_filter.data})


def project_detail(request, name):
    try:
        project = Project.objects.get(name=name)
    except:
        project = None
    return render(request, 'members/project_detail.html', {'project': project})


class CreateProject(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_projects')

    def get(self, request):
        form = ProjectForm()
        return render(request, 'members/create_project_old.html', {'form': form})


class UpdateProject(LoginRequiredMixin, View):
    login_url = 'login_user'
    def post(self, request, pk):
        form = request.POST
        Project.objects.filter(id=pk).update(name=form.get('name'), description=form.get('description'),
                                             active_issue_count=form.get('active_issue_count'),
                                             solved_issue_count=form.get('solved_issue_count'),
                                             start_date=form.get('start_date'), deadline=form.get('deadline'))

        return redirect('show_projects')

    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        form = ProjectForm(instance=project)

        return render(request, 'members/create_project_old.html', {'form': form})


class DeleteProject(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request, pk):
        project = Project.objects.get(id=pk)
        users = User.objects.filter(current_project_id=project.id)
        if users:
            for user in users:
                User.objects.filter(id=user.id).update(current_project_id=None)

        project.delete()
        return redirect('show_projects')

    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        return render(request, 'members/delete_project.html', {'project': project})


class UpdateUser(LoginRequiredMixin, View):
    login_url = 'login_user'
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


class DeleteUser(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()

        return redirect('people')

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        return render(request, 'members/delete_user.html', {'user': user})


class AssignProjectToUser(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        project = Project.objects.get(id=request.POST.get('project'))
        if check_user_project_relation_exist(pk, project.id):
            messages.info(request, 'The project already assigned')
            projects = Project.objects.all()
            return render(request, 'members/assign_project_to_user.html', {'user': user, 'projects': projects})

        UserProjectRelation.objects.create(user=user, project=project)
        project_list = get_user_current_projects(pk)
        User.objects.filter(id=pk).update(project_list=project_list)
        username = None

        return redirect('people')

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        projects = Project.objects.all()
        return render(request, 'members/assign_project_to_user.html', {'user': user, 'projects': projects})


class ShowIssues(LoginRequiredMixin, View):
    login_url = 'login_user'

    def get(self, request):
        # for i in range(20):
        #     name = 'Test'+str(i)
        #     desc = name + 'description'
        #     created_by = request.user.get_username()
        #
        #     Issue.objects.create(name=name,description=desc,opened_by=created_by, is_active=True)

        paginator = Paginator(Issue.objects.all(), 3)
        page = request.GET.get('page')
        issues = paginator.get_page(page)
        print(issues)
        nums = ["page"] * issues.paginator.num_pages

        return render(request, 'members/issues.html', {'issues': issues, 'nums': nums})


class UpdateOrCreateIssue(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request, pk=None):
        form = request.POST
        user = None
        project = None

        if form.get('assigned_to') is not None:
            user = User.objects.get(id=form.get('assigned_to'))
        if form.get('related_project') is not None:
            project = Project.objects.get(id=form.get('assigned_to'))

        is_active = None
        if form.get('is_active') is None:
            is_active = False
        else:
            is_active = True

        if pk == 'None':
            Issue.objects.create(
                name=form.get('name'), description=form.get('description'),
                is_active=is_active,
                related_project=project,
                opened_by=request.user.get_username(),
                assigned_by=request.user.get_username(),
                assignment_date=form.get('assignment_date'),
                assigned_to=user,
                deadline=form.get('deadline'))
        else:
            Issue.objects.filter(id=pk).update(name=form.get('name'), description=form.get('description'),
                                               is_active=is_active,
                                               related_project=project,
                                               assigned_by=request.user.get_username(),
                                               assignment_date=form.get('assignment_date'),
                                               assigned_to=user,
                                               deadline=form.get('deadline'))

        return redirect('issues')

    def get(self, request, pk):
        projects = Project.objects.all()
        users = User.objects.all()

        if pk != "None":
            issue = Issue.objects.get(id=pk)
            form = IssuesForm(instance=issue)
            operation = 'Update'
            return render(request, 'members/update_or_create_issue.html',
                          {'form': form, 'projects': projects, 'users': users,
                           'operation': operation})
        else:
            operation = 'Create'
            form = IssuesForm()
            return render(request, 'members/update_or_create_issue.html',
                          {'form': form, 'projects': projects, 'users': users, 'operation': operation})


class DeleteIssue(LoginRequiredMixin, View):
    login_url = 'login_user'

    def post(self, request, pk):
        issue = Issue.objects.get(id=pk)
        issue.delete()

        return redirect('issues')

    def get(self, request, pk):
        issue = Issue.objects.get(id=pk)
        return render(request, 'members/delete_issue.html', {'issue': issue})


class GetProjectIssues(LoginRequiredMixin, View):
    login_url = 'login_user'

    def get(self, request, pk):
        has_issue = False
        issues = Issue.objects.filter(related_project__id=pk, is_active=True)
        if len(issues) != 0:
            has_issue = True

        return render(request, 'members/get_project_issues.html', {'issues': issues, 'has_issue': has_issue})


class RegisterPage(View):
    def post(self, request):
        form = request.POST
        try:
            User.objects.create_user(form.get('username'), form.get('email'), form.get('password'))
        except:
            messages.error(request, 'User already exist')
            return redirect('register_user')

        messages.success(request, "Account was created for " + form.get('username'))
        return redirect('login_user')

    def get(self, request):
        form = UserForm()
        return render(request, 'members/register.html', {'form': form})

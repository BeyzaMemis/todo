from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.log_out_user, name='logout_user'),
    path('register_user/', views.RegisterPage.as_view(), name='register_user'),
    path('Home/', views.Home, name='home'),
    path('people/', views.People.as_view(), name='people'),
    path('show_user/<user_id>', views.show_user, name='user_detail'),
    path('search_user/', views.SearchUser.as_view(), name='search_user'),
    path('add_user/', views.AddUser.as_view(), name='add_user'),
    path('projects/', views.ShowProjects.as_view(), name='show_projects'),
    path('project_detail/<name>', views.project_detail, name='project_detail'),
    path('create_project', views.CreateProject.as_view(), name='create_project'),
    path('update_project/<str:pk>/', views.UpdateProject.as_view(), name='update_project'),
    path('delete_project/<str:pk>/', views.DeleteProject.as_view(), name='delete_project'),
    path('update_user/<str:pk>', views.UpdateUser.as_view(), name='update_user'),
    path('delete_user/<str:pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('assign_project_to_user/<str:pk>', views.AssignProjectToUser.as_view(), name='assign_project_to_user'),
    path('issues/', views.ShowIssues.as_view(), name='issues'),
    path('update_issue/<str:pk>/', views.UpdateOrCreateIssue.as_view(), name='update_or_create_issue'),
    path('delete_issue/<str:pk>/', views.DeleteIssue.as_view(), name='delete_issue'),
    path('get_project_issues/<str:pk>/', views.GetProjectIssues.as_view(), name='get_project_issues'),


]
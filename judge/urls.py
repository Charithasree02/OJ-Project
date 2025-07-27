from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='judge/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Enable these now
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('problems/create/', views.create_problem, name='create_problem'),

    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('submit/', views.submit_solution, name='submit'),
    path('submissions/', views.submission_list, name='submissions'),

]

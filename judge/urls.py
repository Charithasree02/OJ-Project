from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ import auth views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ✅ Login view using your custom template
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # ✅ Logout view (optional but recommended)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

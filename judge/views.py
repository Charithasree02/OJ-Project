from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Problem

def home(request):
    return render(request, 'judge/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'judge/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'judge/dashboard.html')

@login_required
def problem_list(request):
    problems = Problem.objects.all().order_by('difficulty', 'created_at')
    return render(request, 'judge/problem_list.html', {'problems': problems})

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'judge/problem_detail.html', {'problem': problem})

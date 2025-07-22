from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Problem, Submission
from .forms import SubmissionForm, ProblemForm  # ✅ Make sure both forms are imported

# 🏠 Home page
def home(request):
    return render(request, 'judge/home.html')

# 🧑‍💻 Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'judge/register.html', {'form': form})

# 👤 Dashboard
@login_required
def dashboard(request):
    return render(request, 'judge/dashboard.html')

# 📃 Problem list
@login_required
def problem_list(request):
    problems = Problem.objects.all().order_by('difficulty', 'created_at')
    return render(request, 'judge/problem_list.html', {'problems': problems})

# 🔍 Problem detail & submission
@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            submission.save()
            messages.success(request, '✅ Code submitted successfully!')
            return redirect('problem_detail', problem_id=problem.id)
        else:
            messages.error(request, '❌ Submission failed. Please correct the form.')
    else:
        form = SubmissionForm()

    return render(request, 'judge/problem_detail.html', {'problem': problem, 'form': form})

# 📝 View my submissions
@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'judge/my_submissions.html', {'submissions': submissions})

# ➕ Create new problem (admin-only)
@staff_member_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Problem created successfully.")
            return redirect('problem_list')
        else:
            messages.error(request, "❌ Please fix the errors below.")
    else:
        form = ProblemForm()
    return render(request, 'judge/create_problem.html', {'form': form})

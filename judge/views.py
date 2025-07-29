from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, Submission, TestCase
from .forms import SubmissionForm, ProblemForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from .utils.code_runner import run_code

import json
from django.http import HttpResponse


# -------------------------------
# Home
# -------------------------------
def home(request):
    return render(request, 'judge/home.html')


# -------------------------------
# Register
# -------------------------------
def register(request):
    return render(request, 'register.html')


# -------------------------------
# View: List of all problems
# -------------------------------
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'judge/problem_list.html', {'problems': problems})


# -------------------------------
# View: Problem detail and submission
# -------------------------------
@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    # sample tests = visible to user
    sample_tests = TestCase.objects.filter(problem=problem, is_hidden=False)
    previous_submissions = Submission.objects.filter(
        user=request.user, problem=problem
    ).order_by('-submitted_at')

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            custom_input = request.POST.get('custom_input', '')
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = problem
            submission.verdict = 'Pending'
            submission.save()

            # Run with custom input if provided; else evaluate on all test cases
            if custom_input.strip():
                out, err = run_code(submission.code, submission.language, custom_input)
                submission.output = out
                submission.error = err
                submission.verdict = "Accepted" if not err else "Runtime Error"
                submission.save()
                return redirect('submission_detail', submission_id=submission.pk)
            else:
                # (Your existing full evaluation against all test cases is fine,
                # but if you want to keep it simple, you can leave only custom-run flow.)
                # For now we keep your original evaluation flow:
                test_cases = TestCase.objects.filter(problem=problem)
                all_test_results = []
                all_passed = True
                encountered_runtime_error = False

                for case in test_cases:
                    input_data = case.input_data
                    expected_output = case.expected_output.strip()
                    output, error = run_code(submission.code, submission.language, input_data)

                    if error:
                        all_passed = False
                        encountered_runtime_error = True
                        all_test_results.append({
                            "input": input_data,
                            "expected": expected_output,
                            "output": error,
                            "passed": False,
                            "error": True
                        })
                        break

                    output = output.strip()
                    passed = output == expected_output
                    all_test_results.append({
                        "input": input_data,
                        "expected": expected_output,
                        "output": output,
                        "passed": passed
                    })
                    if not passed:
                        all_passed = False

                submission.test_results_json = json.dumps(all_test_results, indent=2)
                if encountered_runtime_error:
                    submission.verdict = 'Runtime Error'
                    submission.error = all_test_results[-1]["output"]
                elif all_passed:
                    submission.verdict = 'Accepted'
                else:
                    submission.verdict = 'Wrong Answer'
                submission.output = '\n'.join(
                    [r["output"] for r in all_test_results if not r.get("error")]
                )
                submission.save()
                return redirect('submission_detail', submission_id=submission.pk)
    else:
        form = SubmissionForm()

    return render(request, 'judge/problem_detail.html', {
        'problem': problem,
        'form': form,
        'sample_tests': sample_tests,     # <-- matches template name
        'submission': None,
        'previous_submissions': previous_submissions,
    })


# -------------------------------
# View: Submission detail + test results
# -------------------------------
@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    try:
        test_results = json.loads(submission.test_results_json)
    except json.JSONDecodeError:
        test_results = None

    return render(request, 'judge/submission_detail.html', {
        'submission': submission,
        'test_results': test_results
    })


# -------------------------------
# View: Dashboard (optional recent submissions)
# -------------------------------
@login_required
def dashboard(request):
    problems = Problem.objects.all()
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')[:5]
    return render(request, 'judge/dashboard.html', {
        'problems': problems,
        'recent_submissions': submissions
    })


# -------------------------------
# View: All submissions by user
# -------------------------------
@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'judge/my_submissions.html', {'submissions': submissions})


# -------------------------------
# Admin View: Create problem
# -------------------------------
@staff_member_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save()
            return redirect('problem_detail', pk=problem.pk)
    else:
        form = ProblemForm()
    return render(request, 'judge/create_problem.html', {'form': form})


# -------------------------------
# Admin View: All Submissions
# -------------------------------
def submission_list(request):
    submissions = Submission.objects.all()
    return render(request, 'judge/submission_list.html', {'submissions': submissions})


# -------------------------------
# Dummy views (optional)
# -------------------------------
def login_view(request):
    return HttpResponse("Login Page")


def submit_solution(request):
    return HttpResponse("Submit Page")

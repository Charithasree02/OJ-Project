from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, Submission, TestCase
from .forms import SubmissionForm
from .code_runner import run_code

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'judge/problem_list.html', {'problems': problems})

def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    
    # ✅ Use correct field names for test case filtering
    sample_cases = TestCase.objects.filter(problem=problem, is_sample=True, is_hidden=False)
    hidden_cases = TestCase.objects.filter(problem=problem, is_hidden=True)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.user = request.user
            submission.save()

            code = submission.code
            language = submission.language

            test_cases = TestCase.objects.filter(problem=problem)
            all_passed = True
            final_output = ''
            error_output = ''

            for tc in test_cases:
                output, error = run_code(code, language, tc.input_data)

                if error:
                    submission.verdict = 'Runtime Error'
                    submission.error = error
                    all_passed = False
                    break
                elif output.strip() != tc.expected_output.strip():
                    submission.verdict = 'Wrong Answer'
                    submission.output = output
                    all_passed = False
                    break
                else:
                    final_output += f"{output}\n"

            if all_passed:
                submission.verdict = 'Accepted'
                submission.output = final_output.strip()

            submission.save()
            return redirect('submission_detail', submission.pk)
    else:
        form = SubmissionForm()

    return render(request, 'judge/problem_detail.html', {
        'problem': problem,
        'form': form,
        'sample_cases': sample_cases,
        'hidden_cases': hidden_cases,
    })

def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'judge/submission_detail.html', {'submission': submission})

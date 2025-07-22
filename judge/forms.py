from django import forms
from .models import Submission, Problem

# Form for user submissions
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code', 'language']
        widgets = {
            'code': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'placeholder': 'Write your code here...'}),
        }

# NEW: Form for admin to create problems
class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'cols': 80, 'placeholder': 'Problem description...'}),
        }

from django.db import models
from django.contrib.auth.models import User
import json 
LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('cpp', 'C++'),
    ('java', 'Java'),
]

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField(blank=True, null=True)
    output_format = models.TextField(blank=True, null=True)
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=50, default='Easy')
    created_at = models.DateTimeField(auto_now_add=True)
    test_results_json = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)  # Show only sample cases to users

    def __str__(self):
        return f"TestCase for {self.problem.title} ({'Hidden' if self.is_hidden else 'Sample'})"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=20, default='Pending')
    passed_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    output = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.user.username} - {self.problem.title}"

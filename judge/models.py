from django.db import models
from django.contrib.auth.models import User

# Problem Model
class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField(blank=True, null=True)
    output_format = models.TextField(blank=True, null=True)
    constraints = models.TextField(blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# TestCase Model (sample, hidden, etc.)
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    # Flags for type of test case
    is_sample = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=True)  # Hidden by default
    is_custom = models.BooleanField(default=False)  # For user-defined test cases in future

    def __str__(self):
        return f"TestCase for {self.problem.title} ({'Sample' if self.is_sample else 'Hidden'})"

# Submission Model
class Submission(models.Model):
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('C++', 'C++'),
        ('Java', 'Java'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Execution result fields
    verdict = models.CharField(max_length=50, default='Pending')  # Accepted, Wrong Answer, etc.
    output = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.language})"

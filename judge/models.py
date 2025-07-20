from django.db import models

# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard")
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.contrib.auth.models import User

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, default='Python')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s submission for {self.problem.title}"



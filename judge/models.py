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


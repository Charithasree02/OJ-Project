from django.contrib import admin
from .models import Problem, Submission

# You can still register Problem as usual
admin.site.register(Problem)

# Custom admin view for Submission
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'submitted_at')
    list_filter = ('language', 'submitted_at')
    search_fields = ('user__username', 'problem__title')

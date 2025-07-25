from django.contrib import admin
from .models import Problem, Submission, TestCase

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [TestCaseInline]

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'verdict', 'created_at')
    readonly_fields = ('output', 'error')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(TestCase)

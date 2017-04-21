from django.contrib import admin

from assignments.models import Assignment, Question, Subject

class QuestionInline(admin.TabularInline):
    model = Assignment.questions.through

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]

class QuestionAdmin(admin.ModelAdmin):
    pass

class SubjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Assignment, AuthorAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Subject, SubjectAdmin)

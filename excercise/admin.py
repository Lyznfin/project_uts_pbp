from django.contrib import admin
from .models import ExcerciseResult, ExcerciseAnswer, ExcerciseQuestion, CourseExcercise

class AnswerInline(admin.TabularInline):
    model = ExcerciseAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(CourseExcercise)
admin.site.register(ExcerciseQuestion, QuestionAdmin)
admin.site.register(ExcerciseAnswer)
admin.site.register(ExcerciseResult)
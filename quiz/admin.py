from django.contrib import admin
from .models import Subject, Question, QuizAttempt

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question_text', 'correct_option')
    list_filter = ('subject',)
    search_fields = ('question_text',)

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'score', 'date_taken')
    list_filter = ('subject', 'date_taken')
    search_fields = ('user__username',)

admin.site.register(Subject)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
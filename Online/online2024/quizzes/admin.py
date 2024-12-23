from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt

class QuizAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'course', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'quiz', 'question_type')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz', 'question_type')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct',)

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'quiz', 'score', 'attempted_at')
    search_fields = ('student__username', 'quiz__title')
    list_filter = ('quiz', 'student')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)


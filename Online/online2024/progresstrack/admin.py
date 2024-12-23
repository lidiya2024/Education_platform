from django.contrib import admin
from .models import CourseProgress, QuizProgress, StudentProgress

admin.site.register(CourseProgress)
admin.site.register(QuizProgress)
admin.site.register(StudentProgress)

from django.db import models
from django.conf import settings
from courses.models import Course
from quizzes.models import Quiz


class CourseProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_progress')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} progress"

    def update_progress(self, new_progress):
        self.progress_percentage = new_progress
        if self.progress_percentage >= 100:
            self.is_completed = True
        self.save()

class QuizProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_progress')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} progress"

    def update_score(self, new_score):
        self.score = new_score
        if self.score is not None:
            self.is_completed = True
        self.save()


class StudentProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='overall_progress')
    total_courses = models.IntegerField(default=0)
    completed_courses = models.IntegerField(default=0)
    total_quizzes = models.IntegerField(default=0)
    completed_quizzes = models.IntegerField(default=0)
    overall_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Overall progress for {self.student.username}"

    def update_overall_progress(self):
        total_courses = self.student.course_progress.count()
        completed_courses = self.student.course_progress.filter(is_completed=True).count()

        total_quizzes = self.student.quiz_progress.count()
        completed_quizzes = self.student.quiz_progress.filter(is_completed=True).count()

        self.total_courses = total_courses
        self.completed_courses = completed_courses
        self.total_quizzes = total_quizzes
        self.completed_quizzes = completed_quizzes

        course_completion = (completed_courses / total_courses * 100) if total_courses > 0 else 0
        quiz_completion = (completed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0

        self.overall_percentage = (course_completion + quiz_completion) / 2
        self.save()

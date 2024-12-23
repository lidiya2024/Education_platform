from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CourseProgress, QuizProgress, StudentProgress


@login_required
def progress_view(request):
    if request.user.role == 'admin':
        # Admin can view all students' progress
        course_progress = CourseProgress.objects.all()
        quiz_progress = QuizProgress.objects.all()
        overall_progress = StudentProgress.objects.all()
        return render(request, 'progresstrack/admin_progress.html', {
            'course_progress': course_progress,
            'quiz_progress': quiz_progress,
            'overall_progress': overall_progress,
        })

    elif request.user.role == 'instructor':
        # Instructor can view progress of students enrolled in their courses
        course_progress = CourseProgress.objects.filter(course__instructor=request.user)
        quiz_progress = QuizProgress.objects.filter(quiz__course__instructor=request.user)
        student_ids = course_progress.values_list('student', flat=True).distinct()
        overall_progress = StudentProgress.objects.filter(student_id__in=student_ids)
        return render(request, 'progresstrack/instructor_progress.html', {
            'course_progress': course_progress,
            'quiz_progress': quiz_progress,
            'overall_progress': overall_progress,
        })

    else:
        # Students can only view their own progress
        course_progress = CourseProgress.objects.filter(student=request.user)
        quiz_progress = QuizProgress.objects.filter(student=request.user)
        overall_progress = StudentProgress.objects.filter(student=request.user).first()
        return render(request, 'progresstrack/student_progress.html', {
            'course_progress': course_progress,
            'quiz_progress': quiz_progress,
            'overall_progress': overall_progress,
        })

def update_course_progress(student, course, new_progress):
    progress, created = CourseProgress.objects.get_or_create(student=student, course=course)
    progress.update_progress(new_progress)
    return progress

def update_quiz_progress(student, quiz, score):
    quiz_progress, created = QuizProgress.objects.get_or_create(student=student, quiz=quiz)
    quiz_progress.update_score(score)
    return quiz_progress


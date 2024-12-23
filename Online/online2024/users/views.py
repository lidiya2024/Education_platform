from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course, Enrollment
from progresstrack.models import StudentProgress, CourseProgress, QuizProgress
from quizzes.models import Quiz, QuizAttempt
from .forms import UserRegistrationForm, LoginForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('users:admin_dashboard.html')
                elif user.role == 'instructor':
                    return redirect('users:instructor_dashboard.html')
                else:
                    return redirect('users:student_dashboard.html')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide valid login details.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return render(request, '403.html', status=403)  # Optional: restrict access to admins only.

    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_quizzes = Quiz.objects.count()

    # Get recent enrollments and quiz attempts
    recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-enrolled_at')[:5]
    recent_quiz_attempts = QuizAttempt.objects.select_related('student', 'quiz').order_by('-attempted_at')[:5]

    return render(request, 'users/admin_dashboard.html', {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_quizzes': total_quizzes,
        'recent_enrollments': recent_enrollments,
        'recent_quiz_attempts': recent_quiz_attempts,
    })

@login_required
def instructor_dashboard(request):
    if request.user.role != 'instructor':
        return render(request, '403.html', status=403)  # Optional: Redirect unauthorized users.

    courses = Course.objects.filter(instructor=request.user)

    quizzes = Quiz.objects.filter(course__in=courses)

    course_stats = []
    for course in courses:
        enrolled_students = course.enrollments.count()
        course_stats.append({'course': course, 'enrolled_students': enrolled_students})

    return render(request, 'users/instructor_dashboard.html', {
        'courses': courses,
        'quizzes': quizzes,
        'course_stats': course_stats,
    })

@login_required
def student_dashboard(request):

    # Get enrolled courses and their progress
    enrolled_courses = CourseProgress.objects.filter(student=request.user)

    # Get quiz progress for the student
    quiz_progress_list = QuizProgress.objects.filter(student=request.user)

    return render(request, 'users/student_dashboard.html', {
        'user': request.user,
        'enrolled_courses': enrolled_courses,
        'quiz_progress_list': quiz_progress_list,
    })


def login_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'instructor':
            return redirect('instructor_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
    return redirect('login')

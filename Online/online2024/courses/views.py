from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Enrollment, Category


def home(request):
    return render(request, 'home.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists() if request.user.is_authenticated else False
    return render(request, 'courses/course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def create_course(request):
    if request.user.role != 'instructor':
        return redirect('course_list')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')

        if Course.objects.filter(name=title).exists():
            messages.error(request, 'A course with this name already exists.')
        else:
            Course.objects.create(name=title, description=description, image=image)
            messages.success(request, f'Course "{title}" created successfully!')
            return redirect('courses/course_list.html')
    categories = Category.objects.all()
    return render(request, 'courses/create_course.html',{'categories': categories})


@login_required
def enroll_in_course(request, course_id):
    # Get the course object
    course = get_object_or_404(Course, id=course_id)

    # Check if the student is already enrolled in the course
    existing_enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

    if existing_enrollment:
        # If already enrolled, notify the user
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('course_detail', course_id=course.id)

    # Create the new enrollment
    Enrollment.objects.create(student=request.user, course=course)

    # Notify the user that the enrollment was successful
    messages.success(request, 'You have successfully enrolled in the course!')

    return redirect('course_detail', course_id=course.id)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'courses/category_list.html', {'categories': categories})

@login_required
def create_category(request):
    if request.user.role != 'admin':
        return redirect('category_list')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')

        if Category.objects.filter(name=name).exists():
            messages.error(request, 'A category with this name already exists.')
        else:
            Category.objects.create(name=name, description=description, image=image)
            messages.success(request, f'Category "{name}" created successfully!')
            return redirect('courses/category_list.html')

    return render(request, 'courses/create_category.html')

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" has been deleted successfully.')
        return redirect('courses:category_list')

    return render(request, 'courses/delete_category.html', {'category': category})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Course "{course_title}" has been deleted successfully.')
        return redirect('courses:course_list')  # Redirect to your course list view

    return render(request, 'courses/delete_course.html', {'course': course})

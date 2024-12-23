from django.contrib import admin
from .models import Category, Course, Enrollment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'instructor', 'category', 'created_at')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)








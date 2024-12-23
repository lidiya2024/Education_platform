from django.urls import path
from . import views

app_name= 'courses'

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('enroll/<int:course_id>/',views.enroll_in_course, name='enroll_in_course'),
    path('detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('create_course/', views.create_course, name='create_course'),
    path('category_list/', views.category_list, name='category_list'),
    path('create_category/', views.create_category, name='create_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),

]


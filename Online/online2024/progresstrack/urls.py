from django.urls import path
from . import views

app_name = 'progresstrack'

urlpatterns = [
    path('progress/', views.progress_view, name='progress_view'),


]

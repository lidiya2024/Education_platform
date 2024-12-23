from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('courses/', include('courses.urls', namespace='courses')),
    path('users/', include('users.urls', namespace='users')),
    path('quizzes/', include('quizzes.urls', namespace='quizzes')),
    path('progresstrack/', include('progresstrack.urls', namespace='progresstrack')),
    path('certificates/', include('certificates.urls', namespace='certificates')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




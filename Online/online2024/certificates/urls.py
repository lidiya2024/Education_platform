from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('list/', views.CertificateList.as_view(), name='certificate_list'),
    path('detail/<int:pk>/', views.CertificateDetail.as_view(), name='certificate_detail'),
    path('download/<int:pk>/', views.download_certificate, name='download_certificate'),
]

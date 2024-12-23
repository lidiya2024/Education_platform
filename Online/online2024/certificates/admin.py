from django.contrib import admin
from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'certificate_number', 'issued_at']
    search_fields = ['student__username', 'course__title', 'certificate_number']
    list_filter = ['issued_at']

admin.site.register(Certificate, CertificateAdmin)

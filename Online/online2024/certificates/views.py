from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.views.generic import ListView, DetailView
from .models import Certificate


class CertificateList(ListView):
    model = Certificate
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'


class CertificateDetail(DetailView):
    model = Certificate
    template_name = 'certificates/certificate_detail.html'
    context_object_name = 'certificate'


def download_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)

    if certificate.certificate_file:
        response = FileResponse(certificate.certificate_file)
        response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
        return response
    else:
        return HttpResponse("Certificate file not available.", status=404)

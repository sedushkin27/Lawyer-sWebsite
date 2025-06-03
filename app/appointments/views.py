from django.shortcuts import render, get_object_or_404

from services.models import Service

# Create your views here.
def appointments(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {
        'service': service
    }
    return render(request, 'appointments/appointments.html', context)
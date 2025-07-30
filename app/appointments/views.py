from django.shortcuts import render, get_object_or_404

from services.models import Service
from appointments.models import AppointmentDate, AppointmentTime, Reserved_time, Appointment

import json

# Create your views here.
def appointments(request, slug):
    service = get_object_or_404(Service, slug=slug)

    available_dates = AppointmentDate.objects.all()

    available_times = {}
    for date in available_dates:
        reserved_times = Reserved_time.objects.filter(date=date).values_list('time', flat=True)
        times = AppointmentTime.objects.filter(date=date).exclude(time__in=reserved_times).values_list('time', flat=True)
        available_times[str(date.date)] = [time.strftime('%H:%M') for time in times]

    context = {
        'service': service,
        'available_dates': json.dumps([str(date.date) for date in available_dates]),
        'available_times': json.dumps(available_times)
    }

    print(context['available_dates'])
    print(context['available_times'])
    return render(request, 'appointments/appointments.html', context)
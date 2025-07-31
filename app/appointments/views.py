from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from services.models import Service
from appointments.models import AppointmentDate, AppointmentTime, Reserved_time, Appointment

from datetime import datetime

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

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('userstel')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        datetime_str = request.POST.get('datetime_refistration')

        try:
            date, time = datetime_str.split(' ')
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time, '%H:%M').time()

            appointment_date = get_object_or_404(AppointmentDate, date=date_obj)

            if Reserved_time.objects.filter(date=appointment_date, time=time_obj).exists():
                messages.error(request, "Вибраний час вже зарезервовано. Оберіть інший.")
                return redirect('appointments:index', slug=slug)

            reserved_time = Reserved_time.objects.create(date=appointment_date, time=time_obj)

            Appointment.objects.create(
                name=name,
                surname=surname,
                phone=phone,
                email=email,
                comment=comment,
                reserved_time=reserved_time
            )
            return redirect('appointments:index', slug=slug)
        
        except ValueError:
            return redirect('appointments:index', slug=slug)
        except AppointmentDate.DoesNotExist:
            return redirect('appointments:index', slug=slug)

    context = {
        'service': service,
        'available_dates': json.dumps([str(date.date) for date in available_dates]),
        'available_times': json.dumps(available_times)
    }

    return render(request, 'appointments/appointments.html', context)
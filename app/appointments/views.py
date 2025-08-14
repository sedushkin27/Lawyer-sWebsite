from django.shortcuts import render, get_object_or_404, redirect

from services.models import Service
from appointments.models import AppointmentDate, AppointmentTime, Appointment, NeedCallBack

from datetime import datetime

import json

# Create your views here.
def appointments(request, slug):
    service = get_object_or_404(Service, slug=slug)

    available_dates = AppointmentDate.objects.filter(status_date=AppointmentDate.OPEN_ACCESS).distinct()

    available_times = {}
    for date in available_dates:
        times = AppointmentTime.objects.filter(date=date, status=AppointmentTime.NOT_RESERVED).values_list('time', flat=True)
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
            appointment_time = get_object_or_404(AppointmentTime, date=appointment_date, time=time_obj, status=AppointmentTime.NOT_RESERVED)

            Appointment.objects.create(
                name=name,
                surname=surname,
                phone= '+380' + phone,
                email=email,
                comment=comment,
                order_service = service,
                reserved_time=appointment_time
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

def need_call_back(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            NeedCallBack.objects.create(phone= '+380'+phone)
    referer = request.META.get('HTTP_REFERER', 'index')
    return redirect(referer)
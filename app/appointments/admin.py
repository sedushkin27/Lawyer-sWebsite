from django.contrib import admin

from appointments.models import AppointmentDate, AppointmentTime, Reserved_time, Appointment
# Register your models here.

admin.site.register(AppointmentDate)
admin.site.register(AppointmentTime)
admin.site.register(Reserved_time)
admin.site.register(Appointment)

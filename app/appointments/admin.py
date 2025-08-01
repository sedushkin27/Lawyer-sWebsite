from django.contrib import admin

from appointments.models import AppointmentDate, AppointmentTime, Appointment
# Register your models here.

admin.site.register(AppointmentDate)
# admin.site.register(AppointmentTime)
# admin.site.register(Appointment)

@admin.register(AppointmentTime)
class AppointmentTimeAdmin(admin.ModelAdmin):
    list_display = ['time', 'date', 'status']
    list_filter = ['time', 'date', 'status']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone', 'email', 'reserved_time', 'created_at']
    list_filter = ['created_at', 'order_service']
    search_fields = ['name', 'surname', 'phone', 'email']
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['reserved_time'].queryset = AppointmentTime.objects.filter(
            status=AppointmentTime.NOT_RESERVED,
            appointment__isnull=True
        )
        return form
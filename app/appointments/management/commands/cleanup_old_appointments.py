from django.core.management.base import BaseCommand
from django.utils import timezone
from appointments.models import AppointmentDate, AppointmentTime
from datetime import date

class Command(BaseCommand):
    help = 'Видаляє минулі дати та пов’язані часові інтервали з AppointmentDate і AppointmentTime'

    def handle(self, *args, **kwargs):
        today = date.today()

        old_dates = AppointmentDate.objects.filter(date__lt=today)

        for appointment_date in old_dates:
            AppointmentTime.objects.filter(date=appointment_date, status=AppointmentTime.NOT_RESERVED).delete()
            if not appointment_date.appointment_times.exists():
                appointment_date.delete()
                self.stdout.write(self.style.SUCCESS(f'Видалено дату: {appointment_date.date}'))
            
            else:
                appointment_date.status_date = AppointmentDate.OVERDUE
                appointment_date.save()
                self.stdout.write(self.style.WARNING(f'Дата {appointment_date.date} не видалена, оскільки є зарезервовані часові інтервали. Статус змінено на "Прострочено".'))
            
        self.stdout.write(self.style.SUCCESS('Очищення старих прийомів завершено.'))
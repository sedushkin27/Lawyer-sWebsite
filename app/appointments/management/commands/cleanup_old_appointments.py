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

        now_dates = AppointmentDate.objects.filter(date=today).first()
        AppointmentTime.objects.filter(date=now_dates, status=AppointmentTime.NOT_RESERVED).delete()
        if not now_dates.appointment_times.exists():
            now_dates.delete()
            self.stdout.write(self.style.SUCCESS(f'Видалено дату: {now_dates.date}'))
        else:
            now_dates.status_date=AppointmentDate.CLOSED_ACCESS
            appointment_date.save()
            self.stdout.write(self.style.SUCCESS(f'Дата {now_dates.date} оновлена до статусу "Закритий".'))
            
        self.stdout.write(self.style.SUCCESS('Очищення старих прийомів завершено.'))
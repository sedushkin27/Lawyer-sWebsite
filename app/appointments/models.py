from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from datetime import datetime, time

from services.models import Service

phone_validator = RegexValidator(
    regex=r'^\+380\d{9}$',
    message="Номер телефона должен быть в формате +380XXXXXXXXX"
)

class AppointmentDate(models.Model):
    date = models.DateField(("Дата"), auto_now=False, auto_now_add=False)

    class Meta:
        db_table = "appointment_date"
        verbose_name = ("дату")
        verbose_name_plural = ("Дати прийому")

    def __str__(self):
        return str(self.date)
    
class AppointmentTime(models.Model):
    RESERVED = "RESERVED"
    NOT_RESERVED = "NOT_RESERVED"
    RESERVED_STATUS_CHOICES = [
        (RESERVED, "Зарезервовано"),
        (NOT_RESERVED, "Не зарезервовано"),
    ]

    time = models.TimeField(("Час"), auto_now=False, auto_now_add=False)
    date = models.ForeignKey(AppointmentDate, on_delete=models.CASCADE, verbose_name=("Дата"), related_name='appointment_times')
    status = models.CharField(
        max_length=12,
        choices=RESERVED_STATUS_CHOICES,
        default=NOT_RESERVED,
        verbose_name=("Статус резервації")
    )

    class Meta:
        db_table = "appointment_time"
        verbose_name = ("час")
        verbose_name_plural = ("Час прийому")
        unique_together = ['date', 'time']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.date} {str(self.time)}: {self.get_status_display()}"

class Appointment(models.Model):

    name = models.CharField(("Ім'я"), max_length=50)
    surname = models.CharField(("Призвіще"), max_length=50)
    phone = models.CharField(("Телефон"), validators=[phone_validator], max_length=13)
    email = models.EmailField(("Електронна пошта"), max_length=254, null=True, blank=True)
    comment = models.TextField(("Коментар"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Дата створення"))
    order_service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=("Замовлена послуга або консультіция"), related_name='appointments')
    reserved_time = models.OneToOneField(AppointmentTime, on_delete=models.CASCADE, verbose_name=("Зарезервований час"), related_name='appointment')

    class Meta:
        db_table = "client"
        verbose_name = ("клієнт")
        verbose_name_plural = ("Клієнти")

    def __str__(self):
        return f"{self.name} {self.surname} - {self.phone}, зарезервований час: {self.reserved_time.time} {self.reserved_time.date.date}"
    
@receiver(post_save, sender=Appointment)
def set_reserved_status_on_save(sender, instance, created, **kwargs):
    if created and instance.reserved_time:
        instance.reserved_time.status = AppointmentTime.RESERVED
        instance.reserved_time.save()

@receiver(post_delete, sender=Appointment)
def set_reserved_status_on_delete(sender, instance, **kwargs):
    if instance.reserved_time:
        current_datetime = datetime.now()
        appt_date = instance.reserved_time.date.date
        appt_time = instance.reserved_time.time
        appt_datetime = datetime.combine(appt_date, appt_time)
        if appt_datetime <= current_datetime:
            instance.reserved_time.delete()
        else:
            instance.reserved_time.status = AppointmentTime.NOT_RESERVED
            instance.reserved_time.save()

@receiver(post_delete, sender=AppointmentTime)
def delete_appointment_on_time_delete(sender, instance, **kwargs):
    if hasattr(instance, 'appointment') and instance.appointment:
        instance.appointment.delete()

    appointment_date = instance.date
    if not appointment_date.appointment_times.exists():
        appointment_date.delete()
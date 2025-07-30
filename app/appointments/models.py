from django.db import models
from django.core.validators import RegexValidator

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
    time = models.TimeField(("Час"), auto_now=False, auto_now_add=False)
    date = models.ForeignKey(AppointmentDate, on_delete=models.CASCADE, verbose_name=("Дата"), related_name='appointment_times')

    class Meta:
        db_table = "appointment_time"
        verbose_name = ("час")
        verbose_name_plural = ("Час прийому")

    def __str__(self):
        return str(self.time)

class Reserved_time(models.Model):
    time = models.TimeField(("Час"), auto_now=False, auto_now_add=False)
    date = models.ForeignKey(AppointmentDate, on_delete=models.CASCADE, verbose_name=("Дата"), related_name='reserved_times')

    class Meta:
        db_table = "reserved_time"
        verbose_name = ("зарезервовані години")
        verbose_name_plural = ("Зарезервовані години")

    def __str__(self):
        return f"{self.date} {self.time}"

class Appointment(models.Model):

    name = models.CharField(("Ім'я"), max_length=50)
    surname = models.CharField(("Призвіще"), max_length=50)
    phone = models.CharField(validators=[phone_validator], max_length=13)
    email = models.EmailField(("Електронна пошта"), max_length=254)
    comment = models.TextField(("Коментар"))
    reserved_time = models.ForeignKey(Reserved_time, on_delete=models.CASCADE, verbose_name=("Зарезервований час"), related_name = 'reserved_time')

    class Meta:
        db_table = "client"
        verbose_name = ("клієнт")
        verbose_name_plural = ("Клієнти")

    def __str__(self):
        return f"{self.name} {self.surname} - {self.phone}, зарезервований час: {self.reserved_time.time} {self.reserved_time.date.date}"
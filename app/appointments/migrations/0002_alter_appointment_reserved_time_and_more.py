# Generated by Django 4.2.20 on 2025-08-01 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='reserved_time',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.appointmenttime', verbose_name='Зарезервований час'),
        ),
        migrations.AlterUniqueTogether(
            name='appointmenttime',
            unique_together={('date', 'time')},
        ),
        migrations.AddIndex(
            model_name='appointmenttime',
            index=models.Index(fields=['date'], name='appointment_date_id_f97699_idx'),
        ),
    ]

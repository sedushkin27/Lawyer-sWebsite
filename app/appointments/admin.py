from django.contrib import admin
from django import forms
from datetime import datetime, timedelta, date
from appointments.models import AppointmentDate, AppointmentTime, Appointment

class AppointmentDateForm(forms.ModelForm):
    start_date = forms.DateField(
        label="Початкова дата",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label="Кінцева дата",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    weekend_days = forms.MultipleChoiceField(
        label="Вихідні дні",
        choices=[
            ('0', 'Понеділок'),
            ('1', 'Вівторок'),
            ('2', 'Середа'),
            ('3', 'Четвер'),
            ('4', 'П’ятниця'),
            ('5', 'Субота'),
            ('6', 'Неділя'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    specific_weekend_days = forms.CharField(
        label="Конкретні вихідні дні",
        help_text="Введіть дати вихідних днів у форматі YYYY-MM-DD, розділені комами.",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    start_time = forms.TimeField(
        label="Початковий час",
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    end_time = forms.TimeField(
        label="Кінцевий час",
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    interval_minutes = forms.IntegerField(
        label="Інтервал між прийомами (хвилини)",
        initial=30,
        min_value=5,
        max_value=120,
        help_text="Введіть інтервал у хвилинах (від 5 до 120)."
    )
    breaks = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Перерви",
        help_text="Формат: 'HH:MM-HH:MM', розділені комами, наприклад: '12:00-13:00,15:00-15:30'"
    )

    class Meta:
        model = AppointmentDate
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        specific_weekend_days = cleaned_data.get('specific_weekend_days')
        breaks = cleaned_data.get('breaks')
        interval_minutes = cleaned_data.get('interval_minutes')

        # Валидация дат
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Початкова дата не може бути пізніше кінцевої дати.")
            if start_date < date.today():
                raise forms.ValidationError("Початкова дата не може бути в минулому.")

        # Валидация времени
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Початковий час не може бути пізніше або дорівнювати кінцевому часу.")

        # Валидация интервала
        if interval_minutes and interval_minutes < 5:
            raise forms.ValidationError("Інтервал має бути не менше 5 хвилин.")

        # Валидация конкретных выходных дат
        if specific_weekend_days:
            try:
                specific_dates = [datetime.strptime(d.strip(), '%Y-%m-%d').date() for d in specific_weekend_days.split(',') if d.strip()]
                if any(d < start_date or d > end_date for d in specific_dates):
                    raise forms.ValidationError("Конкретні вихідні дні повинні бути в межах діапазону дат.")
                if any(d < date.today() for d in specific_dates):
                    raise forms.ValidationError("Конкретні вихідні дні не можуть бути в минулому.")
            except ValueError:
                raise forms.ValidationError("Неправильний формат дат у конкретних вихідних днях. Використовуйте YYYY-MM-DD.")

        # Валидация перерывов
        if breaks:
            try:
                for break_range in breaks.split(','):
                    if not break_range.strip():
                        continue
                    start, end = break_range.strip().split('-')
                    start = datetime.strptime(start.strip(), '%H:%M').time()
                    end = datetime.strptime(end.strip(), '%H:%M').time()
                    if start >= end:
                        raise forms.ValidationError("Початковий час перерви не може бути пізніше або дорівнювати кінцевому часу.")
                    if start < start_time or end > end_time:
                        raise forms.ValidationError("Перерви повинні бути в межах робочого часу.")
            except ValueError:
                raise forms.ValidationError("Неправильний формат перерв. Використовуйте 'HH:MM-HH:MM'.")

        return cleaned_data

    def save(self, commit=True):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        weekend_days = self.cleaned_data['weekend_days']
        specific_weekend_days = self.cleaned_data['specific_weekend_days']
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        interval_minutes = self.cleaned_data['interval_minutes']
        breaks = self.cleaned_data['breaks']

        # Парсим выходные даты
        weekend_dates = set()
        if specific_weekend_days:
            weekend_dates = {datetime.strptime(d.strip(), '%Y-%m-%d').date() for d in specific_weekend_days.split(',') if d.strip()}
        weekend_days = set(int(day) for day in weekend_days) if weekend_days else set()

        # Парсим перерывы
        break_ranges = []
        if breaks:
            for break_range in breaks.split(','):
                if not break_range.strip():
                    continue
                start, end = break_range.strip().split('-')
                start = datetime.strptime(start.strip(), '%H:%M').time()
                end = datetime.strptime(end.strip(), '%H:%M').time()
                break_ranges.append((start, end))

        # Создаём даты и временные слоты
        created_dates = []
        current_date = start_date
        while current_date <= end_date:
            # Пропускаем выходные и существующие даты
            if (str(current_date.weekday()) in weekend_days or 
                current_date in weekend_dates or 
                AppointmentDate.objects.filter(date=current_date).exists()):
                current_date += timedelta(days=1)
                print("Skipping date:", current_date)
                continue

            # Создаём объект AppointmentDate
            appointment_date = AppointmentDate(date=current_date)
            print("Creating date:", appointment_date.date)
            appointment_date.save()
            created_dates.append(appointment_date)

            # Создаём временные слоты
            current_time = datetime.combine(current_date, start_time)
            end_datetime = datetime.combine(current_date, end_time)
            while current_time < end_datetime:
                time = current_time.time()
                in_break = False
                for break_start, break_end in break_ranges:
                    if break_start <= time < break_end:
                        in_break = True
                        break
                if not in_break:
                    appointment_time = AppointmentTime(
                        date=appointment_date,
                        time=time,
                        status=AppointmentTime.NOT_RESERVED
                    )
                    
                    appointment_time.save()
                current_time += timedelta(minutes=interval_minutes)

            current_date += timedelta(days=1)

        # Возвращаем первый созданный объект AppointmentDate (или None, если ничего не создано)
        return created_dates[0] if created_dates else None

@admin.register(AppointmentDate)
class AppointmentDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'available_times_count']
    list_filter = ['date']
    search_fields = ['date']
    date_hierarchy = 'date'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None: 
            kwargs['form'] = AppointmentDateForm
        else:
            kwargs['form'] = super().get_form(request, obj, **kwargs)
        return super().get_form(request, obj, **kwargs)

    def save_related(self, request, form, formsets, change):
        if not isinstance(form, AppointmentDateForm):
            super().save_related(request, form, formsets, change)

    def available_times_count(self, obj):
        return obj.appointment_times.filter(status=AppointmentTime.NOT_RESERVED).count()
    available_times_count.short_description = 'Кількість доступних часів'

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
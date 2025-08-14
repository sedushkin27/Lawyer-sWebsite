from django.contrib import admin
from django import forms
from datetime import datetime, timedelta, date
from appointments.models import AppointmentDate, AppointmentTime, Appointment, NeedCallBack

class AppointmentDateForm(forms.ModelForm):
    MODE_CHOICES = (
        ('single', 'Одна дата'),
        ('range', 'Діапазон дат'),
    )
    mode = forms.ChoiceField(
        label="Режим створення",
        choices=MODE_CHOICES,
        widget=forms.RadioSelect,
        initial='single'
    )
    single_date = forms.DateField(
        label="Дата",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    start_date = forms.DateField(
        label="Початкова дата",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        label="Кінцева дата",
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
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
        mode = cleaned_data.get('mode')
        single_date = cleaned_data.get('single_date')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        specific_weekend_days = cleaned_data.get('specific_weekend_days')
        breaks = cleaned_data.get('breaks')
        interval_minutes = cleaned_data.get('interval_minutes')

        if interval_minutes and interval_minutes < 5:
            raise forms.ValidationError("Інтервал має бути не менше 5 хвилин.")

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Початковий час не може бути пізніше або дорівнювати кінцевому часу.")

        if mode == 'single':
            if not single_date:
                raise forms.ValidationError("Для режиму 'Одна дата' необхідно вказати дату.")
            if single_date < date.today():
                raise forms.ValidationError("Дата не може бути в минулому.")
            if AppointmentDate.objects.filter(date=single_date).exists():
                raise forms.ValidationError("Ця дата вже існує.")
        else:  # mode == 'range'
            if not start_date or not end_date:
                raise forms.ValidationError("Для режиму 'Діапазон дат' необхідно вказати початкову та кінцеву дати.")
            if start_date > end_date:
                raise forms.ValidationError("Початкова дата не може бути пізніше кінцевої дати.")
            if start_date < date.today():
                raise forms.ValidationError("Початкова дата не може бути в минулому.")

        if specific_weekend_days:
            try:
                specific_dates = [datetime.strptime(d.strip(), '%Y-%m-%d').date() for d in specific_weekend_days.split(',') if d.strip()]
                if mode == 'single':
                    if any(d == single_date for d in specific_dates):
                        raise forms.ValidationError("Дата не може бути вказана як вихідний день.")
                else:
                    if any(d < start_date or d > end_date for d in specific_dates):
                        raise forms.ValidationError("Конкретні вихідні дні повинні бути в межах діапазону дат.")
                if any(d < date.today() for d in specific_dates):
                    raise forms.ValidationError("Конкретні вихідні дні не можуть бути в минулому.")
            except ValueError:
                raise forms.ValidationError("Неправильний формат дат у конкретних вихідних днях. Використовуйте YYYY-MM-DD.")

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
        mode = self.cleaned_data['mode']
        single_date = self.cleaned_data['single_date']
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

        break_ranges = []
        if breaks:
            for break_range in breaks.split(','):
                if not break_range.strip():
                    continue
                start, end = break_range.strip().split('-')
                start = datetime.strptime(start.strip(), '%H:%M').time()
                end = datetime.strptime(end.strip(), '%H:%M').time()
                break_ranges.append((start, end))

        created_dates = []
        if mode == 'single':
            dates = [single_date]
        else:
            dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        for current_date in dates:
            print(current_date.weekday())
            print(weekend_days)
            if int(current_date.weekday() in weekend_days or 
                current_date in weekend_dates or 
                AppointmentDate.objects.filter(date=current_date).exists()):
                continue

            appointment_date = AppointmentDate(date=current_date)
            
            appointment_date.save()
            created_dates.append(appointment_date)

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

        return created_dates[0] if created_dates else None

class AppointmentTimeInline(admin.TabularInline):
    model = AppointmentTime
    extra = 0
    fields = ['time', 'status']

@admin.action(description="Позначте вибрані дати як відкриті для запису")
def mark_as_open_access(modeladmin, request, queryset):
    queryset.update(status_date=AppointmentDate.OPEN_ACCESS)

@admin.action(description="Позначте вибрані дати як закриті для запису")
def mark_as_closed_access(modeladmin, request, queryset):
    queryset.update(status_date=AppointmentDate.CLOSED_ACCESS)


@admin.action(description="Видалити час прийому (не зарезервований)")
def delete_unreserved_times(modeladmin, request, queryset):
    for appointment_date in queryset:
        AppointmentTime.objects.filter(date=appointment_date, status=AppointmentTime.NOT_RESERVED).delete()
        if not appointment_date.appointment_times.exists():
            appointment_date.delete()
            modeladmin.message_user(request, f'Видалено дату: {appointment_date.date}')
        else:
            appointment_date.update(status_date=AppointmentDate.OVERDUE)
            modeladmin.message_user(request, f'Дата {appointment_date.date} не видалена, оскільки є зарезервовані часові інтервали.', level='warning')

@admin.register(AppointmentDate)
class AppointmentDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'available_times_count', 'status_date']
    list_filter = ['date', 'status_date']
    search_fields = ['date']
    date_hierarchy = 'date'
    actions = [mark_as_open_access, mark_as_closed_access, delete_unreserved_times]

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  
            kwargs['form'] = AppointmentDateForm
        else: 
            kwargs['form'] = super().get_form(request, obj, **kwargs)
            self.inlines = [AppointmentTimeInline]
        return super().get_form(request, obj, **kwargs)

    def save_related(self, request, form, formsets, change):
        if not isinstance(form, AppointmentDateForm):
            super().save_related(request, form, formsets, change)

    def get_changeform_initial_data(self, request):
        return {'mode': 'single'}

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_dynamic_fields'] = True
        return super().changeform_view(request, object_id, form_url, extra_context)

    def available_times_count(self, obj):
        return obj.appointment_times.filter(status=AppointmentTime.NOT_RESERVED).count()
    available_times_count.short_description = 'Кількість доступних часів'

@admin.register(AppointmentTime)
class AppointmentTimeAdmin(admin.ModelAdmin):
    list_display = ['time', 'date', 'month', 'day', 'status']
    list_filter = ['date', 'status'] 
    search_fields = ['date__date', 'time']
    ordering = ['date__date', 'time']

    def month(self, obj):
        """Отображает месяц из связанной даты."""
        return obj.date.date.strftime('%B') if obj.date else '-'
    month.short_description = 'Місяць'
    month.admin_order_field = 'date__date' 

    def day(self, obj):
        """Отображает день из связанной даты."""
        return obj.date.date.day if obj.date else '-'
    day.short_description = 'День'
    day.admin_order_field = 'date__date' 

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
    
@admin.register(NeedCallBack)
class NeedCallBackAdmin(admin.ModelAdmin):
    list_display = ['phone', 'created_at']
    search_fields = ['phone']
    ordering = ['-created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
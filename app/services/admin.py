from django.contrib import admin
from django.utils.text import slugify
from django import forms

# Register your models here.
from services.models import Service, ServiceSection, SectionItem

# admin.site.register(Services)
admin.site.register(ServiceSection)
admin.site.register(SectionItem)
class ServiceSectionForm(forms.ModelForm):
    items_text = forms.CharField(
        label="Елементи списку (по одному на рядок)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введіть елементи списку, кожен з нового рядка'})
    )

    class Meta:
        model = ServiceSection
        fields = ['title', 'items_text']

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if self.cleaned_data['items_text']:
            # Удаляем существующие элементы перед добавлением новых
            instance.items.all().delete()
            # Создаем новые элементы на основе текста
            items = [item.strip() for item in self.cleaned_data['items_text'].split('\n') if item.strip()]
            for item_text in items:
                SectionItem.objects.create(section=instance, text=item_text)
        return instance

class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 0  # Не добавляем пустые формы, так как они создаются динамически
    fields = ['text']
    can_delete = True

class ServiceSectionInline(admin.TabularInline):
    model = ServiceSection
    extra = 1  # Количество пустых форм для добавления новых секций
    form = ServiceSectionForm
    fields = ['title', 'items_text']

@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'service_type']
    list_filter = ['title', 'price', 'service_type']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceSectionInline]

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)
from django.contrib import admin
from django.utils.text import slugify
from django import forms

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            items = self.instance.items.all()
            self.initial['items_text'] = '\n'.join(item.text for item in items)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if self.cleaned_data['items_text']:
            instance.items.all().delete()
            items = [item.strip() for item in self.cleaned_data['items_text'].split('\n') if item.strip()]
            for item_text in items:
                SectionItem.objects.create(section=instance, text=item_text)
        return instance

class SectionItemInline(admin.TabularInline):
    model = SectionItem
    extra = 0 
    fields = ['text']
    can_delete = True

class ServiceSectionInline(admin.TabularInline):
    model = ServiceSection
    extra = 0 
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
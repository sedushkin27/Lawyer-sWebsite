from django.contrib import admin

# Register your models here.
from services.models import Service, ServiceSection, SectionItem

# admin.site.register(Services)
admin.site.register(ServiceSection)
admin.site.register(SectionItem)

@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'service_type']
    list_filter = ['title', 'price', 'service_type']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
from django.contrib import admin

# Register your models here.
from services.models import Service, ServiceSection, SectionItem

# admin.site.register(Services)
admin.site.register(ServiceSection)
admin.site.register(SectionItem)

@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
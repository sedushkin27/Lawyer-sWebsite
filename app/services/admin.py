from django.contrib import admin

# Register your models here.
from services.models import Services, ServiceSection, SectionItem

# admin.site.register(Services)
admin.site.register(ServiceSection)
admin.site.register(SectionItem)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
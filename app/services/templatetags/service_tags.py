from django import template

from services.models import Service

register = template.Library()

@register.simple_tag()
def first_slug_service():
    return Service.objects.filter(service_type='service').values("slug").first()

@register.simple_tag()
def first_slug_consultation():
    return Service.objects.filter(service_type='consultation').values("slug").first()
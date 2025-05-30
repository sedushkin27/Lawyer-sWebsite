from django import template

from services.models import Service

register = template.Library()

@register.simple_tag()
def first_slug_service():
    return Service.objects.values("slug").first()
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from services.models import Service

# Create your views here.
def services(request, slug):
    service = get_object_or_404(Service.objects.prefetch_related(
        Prefetch('sections__items')  # Получить секции и вложенные пункты
    ), slug=slug)
    another_services = Service.objects.exclude(pk=service.pk).only('title', 'slug')
    context = {
        'service': service,
        'another_services': another_services,
    }
    return render(request, 'service/service.html', context)
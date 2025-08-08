from django.http import HttpResponse
from django.shortcuts import render

from services.models import Service
from main.models import Review, PrivacyPolicy

# Create your views here.
def index(request):

    services = Service.objects.filter(service_type='service').only('title', 'slug', 'image')
    consultations = Service.objects.filter(service_type='consultation').only('title', 'slug', 'image')
    rewiews = Review.objects.all()

    context = {
        'services': services,

        'consultations': consultations,

        'reviews': rewiews,
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        
    }
    return render(request, 'main/about_me.html')

def conditioning_policy(request):
    policy = PrivacyPolicy.objects.first()  # Берем первую запись
    context = {
        'policy': policy,
    }
    return render(request, 'main/conditioning_policy.html', context)
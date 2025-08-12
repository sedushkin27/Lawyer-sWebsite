from django.http import HttpResponse
from django.shortcuts import render

from services.models import Service
from main.models import Review, LegalDocument, AboutMe, AdvantagesWorkingWithMe

# Create your views here.
def index(request):

    about_me = AboutMe.objects.only('name', 'sername', 'main_about_me_text', 'first_photo', 'second_photo', 'third_photo', 'phone', 'email', 'address', 'years_of_experience', 'winning_cases_count', 'client_count', 'telegram', 'viber', 'messenger', 'whatsapp').first()
    advantages_working_with_me = AdvantagesWorkingWithMe.objects.filter(about_me=about_me).only('title', 'text')
    services = Service.objects.filter(service_type='service').only('title', 'slug', 'image')
    consultations = Service.objects.filter(service_type='consultation').only('title', 'slug', 'image')
    rewiews = Review.objects.all()

    context = {
        'about_me': about_me,
        'advantages_working_with_me': advantages_working_with_me,

        'services': services,

        'consultations': consultations,

        'reviews': rewiews,
    }
    return render(request, 'main/index.html', context)

def about(request):
    about_me = AboutMe.objects.only('name', 'sername', 'other_about_me_text', 'second_photo').first()
    advantages_working_with_me = AdvantagesWorkingWithMe.objects.filter(about_me=about_me).only('title', 'text')
    context = {
        'about_me': about_me,
        'advantages_working_with_me': advantages_working_with_me,
    }
    return render(request, 'main/about_me.html', context)

def conditioning_policy(request):
    policy = LegalDocument.objects.filter(document_type='privacy_policy').first()
    context = {
        'legal_document': policy,
    }
    return render(request, 'main/legal_document.html', context)

def public_offer(request):
    offer = LegalDocument.objects.filter(document_type='public_offer').first()
    context = {
        'legal_document': offer,
    }
    return render(request, 'main/legal_document.html', context)
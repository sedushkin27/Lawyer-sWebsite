from django.urls import path

from services.views import services, consultation

app_name = 'services'

urlpatterns = [
    path('<slug:slug>/', services, name='index'),
    path('consultation/<slug:slug>/', consultation, name='consultation'),
]
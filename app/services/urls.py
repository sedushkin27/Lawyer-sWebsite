from django.urls import path

from services.views import services

app_name = 'services'

urlpatterns = [
    path('', services, name='index')
]
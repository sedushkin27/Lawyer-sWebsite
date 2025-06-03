from django.urls import path

from appointments.views import appointments

app_name = 'appointments'

urlpatterns = [
    path('<slug:slug>/', appointments, name='index'),
]
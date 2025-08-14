from django.urls import path

from appointments.views import appointments, need_call_back

app_name = 'appointments'

urlpatterns = [
    path('need-call-back/', need_call_back, name='need_call_back'),
    path('<slug:slug>/', appointments, name='index'),
]
from django.urls import path

from main.views import index, about, conditioning_policy

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about-me/', about, name='about'),
    path('conditioning-policy/', conditioning_policy, name='conditioning_policy')
]
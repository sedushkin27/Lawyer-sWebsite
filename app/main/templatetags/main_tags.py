from django import template

from main.models import AboutMe

register = template.Library()

@register.simple_tag()
def get_social_media():
    about_me = AboutMe.objects.only('facebook', 'instagram', 'tiktok').first()
    if not about_me:
        return {}
    
    social_media = {
        'facebook': about_me.facebook,
        'instagram': about_me.instagram,
        'tiktok': about_me.tiktok,
    }
    
    return {key: value for key, value in social_media.items() if value}
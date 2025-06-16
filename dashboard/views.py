from django.shortcuts import render
from datetime import date
from .models import NavBar, Banner, SMEStep, Service, Guidelines, NewsEvent, ContactInfo, Quicklinks, SocialLinks

def landing_page(request):
    navbar_content = NavBar.objects.all()

    banners = Banner.objects.all().order_by("order")

    steps = SMEStep.objects.all()[:4]

    services= Service.objects.all()[:3]

    guidelines = Guidelines.objects.all()[:4]

    today = date.today()
    events = NewsEvent.objects.filter(start_date__lte=today, end_date__gte=today).order_by('-start_date')

    contact_infos = ContactInfo.objects.all()

    quick_links = Quicklinks.objects.all()

    social_links = SocialLinks.objects.all



    context = {
        'navbar_content': navbar_content,
        'banners': banners,
        'steps': steps,
        'services': services,
        'guidelines': guidelines,
        'news_events': events,
        'today': today,
        'contact_infos': contact_infos,
        'quick_links': quick_links,
        'social_links': social_links,
    }
    return render(request, "landing.html", context)

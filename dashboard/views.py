from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Banner, SMEStep, Service, Guidelines, NewsEvent, ContactInfo, Quicklinks, SocialLinks, Notice, MenuItem, CMSPage

def landing_page(request):
    menu_items = MenuItem.objects.filter(parent=None).prefetch_related('children').order_by('order')

    banners = Banner.objects.all()

    steps = SMEStep.objects.all()[:4]

    services= Service.objects.all()[:3]

    guidelines = Guidelines.objects.all()[:4]

    today = date.today()
    events = NewsEvent.objects.filter(start_date__lte=today, end_date__gte=today).order_by('-start_date')

    contact_infos = ContactInfo.objects.all()

    quick_links = Quicklinks.objects.all()

    social_links = SocialLinks.objects.all()

    popup_notices = Notice.objects.filter(is_popup=True).order_by('popup_order')



    context = {
        'menu_items': menu_items,
        'banners': banners,
        'steps': steps,
        'services': services,
        'guidelines': guidelines,
        'news_events': events,
        'today': today,
        'contact_infos': contact_infos,
        'quick_links': quick_links,
        'social_links': social_links,
        'popup_notices': popup_notices,
    }
    return render(request, "landing.html", context)


def notice_list(request):
    notices = Notice.objects.all().order_by('created_at')
    return render(request, 'notice_list.html', {'notices': notices})

def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    return render(request, 'notice_detail.html', {'notice': notice})

def service_list(request):
    services = Service.objects.all().order_by('order')
    return render(request,'service_list.html', {'services': services})

def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'service_detail.html', {'service': service})


def news_list(request):
    today = date.today()
    news_events = NewsEvent.objects.filter(start_date__lte=today, end_date__gte=today).order_by('-start_date')
    return render(request, 'news_list.html', {
        'news_events': news_events,
        'today': today,
    })

def news_detail(request, id):
    event = get_object_or_404(NewsEvent, id=id)
    return render(request, 'news_detail.html', {
        'event': event,
    })


def cms_page_detail(request, slug):
    page = get_object_or_404(CMSPage, slug=slug)
    return render(request, 'cms/page_detail.html', {'page': page})



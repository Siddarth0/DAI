from django.shortcuts import render
from .models import NavBar, Banner, SMEStep, Service, Guidelines

def landing_page(request):
    navbar_content = NavBar.objects.first()
    banners = Banner.objects.all().order_by("order")

    steps = SMEStep.objects.all()[:4]

    services= Service.objects.all()[:3]

    guidelines = Guidelines.objects.all()[:4]



    context = {
        'navbar_content': navbar_content,
        'banners': banners,
        'steps': steps,
        'services': services,
        'guidelines': guidelines,
    }
    return render(request, "landing.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from datetime import date

from .models import (
    Banner, SMEStep, Service, Guidelines, NewsEvent, Notice, CMSPage
)

from django.forms import modelform_factory
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import get_all_models
from dashboard.forms import FORM_MAP
from django.contrib import messages


def landing_page(request):
    banners = Banner.objects.filter(is_active=True)
    steps = SMEStep.objects.all()[:4]
    services = Service.objects.all()[:3]
    guidelines = Guidelines.objects.all()[:4]

    today = date.today()
    events = NewsEvent.objects.filter(start_date__lte=today, end_date__gte=today).order_by('-start_date')
    
    popup_notices = Notice.objects.filter(is_popup=True).order_by('popup_order')

    context = {
        'banners': banners,
        'steps': steps,
        'services': services,
        'guidelines': guidelines,
        'news_events': events,
        'today': today,
        'popup_notices': popup_notices,
    }
    return render(request, "landing.html", context)


def notice_list(request):
    notices = Notice.objects.all().order_by('created_at')
    return render(request, 'notice/notice_list.html', {'notices': notices})

def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    return render(request, 'notice/notice_detail.html', {'notice': notice})

def service_list(request):
    services = Service.objects.all().order_by('order')
    return render(request, 'service/service_list.html', {'services': services})

def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'service/service_detail.html', {'service': service})

def news_list(request):
    today = date.today()
    news = NewsEvent.objects.filter(category='news').order_by('-start_date')
    

    webinars = NewsEvent.objects.filter(category='webinar', start_date__lte=today, end_date__gte=today).order_by('-start_date')
    events = NewsEvent.objects.filter(category='event', start_date__lte=today, end_date__gte=today).order_by('-start_date')
    return render(request, 'news/news_list.html', {
        'news': news,
        'webinars': webinars,
        'events': events,
        'today': today,
    })

def news_detail(request, pk):
    event = get_object_or_404(NewsEvent, pk=pk)
    today = date.today()

    # Get similar category events excluding current one
    similar_events = NewsEvent.objects.filter(
        category=event.category,
        start_date__lte=today,
        end_date__gte=today
    ).exclude(pk=pk).order_by('-start_date')[:5]

    return render(request, 'news/news_detail.html', {
        'event': event,
        'today': today,
        'similar_events': similar_events,
    })


def cms_page_detail(request, slug):
    page = get_object_or_404(CMSPage, slug=slug)
    return render(request, 'cms/page_detail.html', {'page': page})


@login_required
def dashboard_home(request):
    models = get_all_models()
    return render(request, 'adminDashboard/index.html', {'models': models})


@login_required
def model_list(request, model_name):
    model_info = get_all_models().get(model_name)
    if not model_info:
        return redirect('dashboard:dashboard_home') 
    
    model = model_info['model']  # <-- extract the model class here

    search_query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '-id')
    queryset = model.objects.all().order_by(order_by)

    if search_query:
        fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField']]
        queries = Q()
        for field in fields:
            queries |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(queries)

    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    all_fields = [f.name for f in model._meta.fields]
    has_is_active = 'is_active' in all_fields
    fields = [f for f in all_fields if f not in ('id', 'is_active', 'created_at', 'updated_at')]

    return render(request, 'adminDashboard/model_list.html', {
        'model': model,
        'objects': page_obj,
        'model_name': model_name,
        'current_model_name': model_name,
        'fields': fields,
        'has_is_active': has_is_active,
        'search_query': search_query,
        'verbose_name': model_info['verbose_name'],  # optionally pass for template
        'verbose_name_plural': model_info['verbose_name_plural'],  # optionally pass for template
    })

@login_required
def model_add(request, model_name):
    model_info = get_all_models().get(model_name)
    if not model_info:
        return redirect('dashboard:dashboard_home')

    model = model_info['model']  # ✅ Extract actual model class

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[f.name for f in model._meta.fields if f.editable and f.name != 'id'])

    form = FormClass(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:model_list', model_name=model_name)

    return render(request, 'adminDashboard/model_form.html', {
        'form': form,
        'model_name': model_name,
        'current_model_name': model_name,
        'mode': 'Add',
    })


@login_required
def model_edit(request, model_name, pk):
    model_info = get_all_models().get(model_name)  # ✅ model_info is a dict
    if not model_info:
        return redirect('dashboard:dashboard_home')

    model = model_info['model']  # ✅ Get actual model class

    instance = get_object_or_404(model, pk=pk)

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[
            f.name for f in model._meta.fields if f.editable and f.name != 'id'
        ])

    form = FormClass(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:model_list', model_name=model_name)

    return render(request, 'adminDashboard/model_form.html', {
        'form': form,
        'model_name': model_name,
        'current_model_name': model_name,
        'mode': 'Edit',
    })

@login_required
def model_delete(request, model_name, pk):
    model_info = get_all_models().get(model_name)
    if not model_info:
        return redirect('dashboard:dashboard_home')

    model = model_info['model']  # ✅ Extract the actual model class

    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        # Find child relationships
        for related in model._meta.related_objects:
            related_name = related.get_accessor_name()
            related_queryset = getattr(instance, related_name).all()

            if related_queryset.exists():
                rel_model = related.related_model
                field_name = related.field.name

                # Try to get or create "Others" instance (must exist per model!)
                others_obj, created = model.objects.get_or_create(name="Others")

                # Reassign children
                related_queryset.update(**{field_name: others_obj})

        instance.delete()
        return redirect('dashboard:model_list', model_name=model_name)

    return redirect('dashboard:model_list', model_name=model_name)


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url or 'dashboard:dashboard_home')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'authys/login.html')


def welcome_page(request):
    return render(request, 'authys/welcomePage.html')

def sme_registration(request):
    return render(request, 'register/sme.html')

def bdsp_registration(request):
    return render(request, 'register/bdsp.html')


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
    news_events = NewsEvent.objects.filter(start_date__lte=today, end_date__gte=today).order_by('-start_date')
    return render(request, 'news/news_list.html', {
        'news_events': news_events,
        'today': today,
    })

def news_detail(request, id):
    event = get_object_or_404(NewsEvent, id=id)
    return render(request, 'news/news_detail.html', {'event': event})


def cms_page_detail(request, slug):
    page = get_object_or_404(CMSPage, slug=slug)
    return render(request, 'cms/page_detail.html', {'page': page})


@login_required
def dashboard_home(request):
    models = get_all_models()
    return render(request, 'adminDashboard/index.html', {'models': models})


@login_required
def model_list(request, model_name):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('dashboard:dashboard_home') 

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
    fields = [f for f in all_fields if f not in ('id', 'is_active','created_at', 'updated_at')]

    return render(request, 'adminDashboard/model_list.html', {
        'model': model,
        'objects': page_obj,
        'model_name': model_name,
        'current_model_name': model_name,
        'fields': fields,
        'has_is_active': has_is_active,
        'search_query': search_query,
    })


@login_required
def model_add(request, model_name):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('dashboard:dashboard_home')  # fixed

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[f.name for f in model._meta.fields if f.editable and f.name != 'id'])

    form = FormClass(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:model_list', model_name=model_name)  # fixed

    return render(request, 'adminDashboard/model_form.html', {
        'form': form,
        'model_name': model_name,
        'current_model_name': model_name,
        'mode': 'Add',
    })


@login_required
def model_edit(request, model_name, pk):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('dashboard:dashboard_home')  # fixed

    instance = get_object_or_404(model, pk=pk)

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[f.name for f in model._meta.fields if f.editable and f.name != 'id'])

    form = FormClass(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:model_list', model_name=model_name)  # fixed

    return render(request, 'adminDashboard/model_form.html', {
        'form': form,
        'model_name': model_name,
        'current_model_name': model_name,
        'mode': 'Edit',
    })


@login_required
def model_delete(request, model_name, pk):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('dashboard:dashboard_home')

    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        # Find child relationships
        for related in model._meta.related_objects:
            related_name = related.get_accessor_name()
            related_queryset = getattr(instance, related_name).all()

            # If there are children, move them to "Others"
            if related_queryset.exists():
                rel_model = related.related_model
                field_name = related.field.name  # usually 'parent'

                # Try to get or create "Others" instance (must exist per model!)
                others_obj, created = model.objects.get_or_create(name="Others")

                # Reassign all children to the "Others" item
                related_queryset.update(**{field_name: others_obj})

        instance.delete()
        return redirect('dashboard:model_list', model_name=model_name)

    # Fallback, shouldn't reach here since deletion is now modal
    return redirect('dashboard:model_list', model_name=model_name)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:dashboard_home')  # fixed
            return redirect('dashboard:landing_page')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'authys/login.html')

    return render(request, 'authys/login.html')


def welcome_page(request):
    return render(request, 'authys/welcomePage.html')








# //cms CMSPage
# //truncate words
# //verbose menuitems
# //sankkefiy admin titles
# //learn more if we can simplfy passing the context since we are passing every context from the views
# start date end date,, add logic to prevent enetering old startdate than today
# no need to show created at updated at at admin
# add paginations on the lists
# is active button needed for notices/ banners/ wherever necessary
# learn more about [:4] what it does, what if we want to access the last items? waht if [: 1,2,5]
# in the content field, add WYSIWYG editor
# merge all apps and porevent making the apps unnecessarily
# categorize the news instead of tags
# add * to mark compulsory fields
# a child can never be the parent of its parent
# when deleting any items, instead of redirecting , popup display( for parent containing child, deleteing parent should popup a warning shwoing what it might afffect)
# when parent contating children is deleted, it should automatically shift to a auto built other item .
# def get_absolute_url learn about it, what is this function called. 
# separate list choices from the logic into a separate component
# 


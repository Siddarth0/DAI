from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import get_all_models
from dashboard.forms import FORM_MAP

@login_required
def dashboard_home(request):
    models = get_all_models()
    return render(request, 'adminDashboard/index.html', {'models': models})


@login_required
def model_list(request, model_name):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('adminDashboard:dashboard_home')

    search_query = request.GET.get('q', '')
    queryset = model.objects.all()

    if search_query:
        fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField']]
        queries = Q()
        for field in fields:
            queries |= Q(**{f"{field}__icontains": search_query})
        queryset = queryset.filter(queries)

    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'adminDashboard/model_list.html', {
        'model': model,
        'objects': page_obj,
        'model_name': model_name,
        'current_model_name': model_name,
        'fields': [f.name for f in model._meta.fields],
        'search_query': search_query,
    })


@login_required
def model_add(request, model_name):
    model = get_all_models().get(model_name)
    if not model:
        return redirect('adminDashboard:dashboard_home')

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[f.name for f in model._meta.fields if f.editable and f.name != 'id'])

    form = FormClass(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('adminDashboard:model_list', model_name=model_name)

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
        return redirect('adminDashboard:dashboard_home')

    instance = get_object_or_404(model, pk=pk)

    FormClass = FORM_MAP.get(model_name)
    if not FormClass:
        FormClass = modelform_factory(model, fields=[f.name for f in model._meta.fields if f.editable and f.name != 'id'])

    form = FormClass(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('adminDashboard:model_list', model_name=model_name)

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
        return redirect('adminDashboard:dashboard_home')

    instance = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        instance.delete()
        return redirect('adminDashboard:model_list', model_name=model_name)

    return render(request, 'adminDashboard/model_confirm_delete.html', {
        'object': instance,
        'model_name': model_name,
        'current_model_name': model_name,
    })
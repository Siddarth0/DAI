from django.urls import get_resolver, URLPattern, URLResolver
from django.apps import apps
from dashboard.templatetags.dashboard_tags import snake_to_title


def extract_named_urls(resolver=None, namespace_prefix=''):
    if resolver is None:
        resolver = get_resolver()

    named_urls = []

    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLPattern) and pattern.name:
            full_name = f'{namespace_prefix}{pattern.name}' if namespace_prefix else pattern.name

            # Exclude admin and old app namespaces
            if full_name.startswith('admin:') or full_name.startswith('authys:') or full_name.startswith('adminDashboard:'):
                continue

            # Get only the last part after colon for label, e.g., "landing_page"
            url_name = full_name.split(":")[-1]

            # Convert snake_case to Title Case for label
            label = snake_to_title(url_name)

            named_urls.append((full_name, label))

        elif isinstance(pattern, URLResolver):
            sub_namespace = f'{namespace_prefix}{pattern.namespace}:' if pattern.namespace else namespace_prefix
            named_urls.extend(extract_named_urls(pattern, sub_namespace))

    return named_urls



def get_all_models(app_labels=['dashboard']):
    all_models = {}
    for label in app_labels:
        app_models = apps.get_app_config(label).get_models()
        for model in app_models:
            all_models[model.__name__.lower()] = {
                'model': model,
                'verbose_name': model._meta.verbose_name.title(),  # or capfirst
                'verbose_name_plural': model._meta.verbose_name_plural.title(),
            }
    return all_models
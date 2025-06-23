from django.urls import get_resolver, URLPattern, URLResolver

def extract_named_urls(resolver=None, namespace_prefix=''):
    if resolver is None:
        resolver = get_resolver()

    named_urls = []

    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLPattern) and pattern.name:
            full_name = f'{namespace_prefix}{pattern.name}' if namespace_prefix else pattern.name

            if full_name.startswith('admin:') or full_name.startswith('adminDashboard:'):
                continue

            # Display only name in label, store full name as value
            label = full_name.split(":")[-1]  # e.g., "service_detail"
            named_urls.append((full_name, label))

        elif isinstance(pattern, URLResolver):
            sub_namespace = f'{namespace_prefix}{pattern.namespace}:' if pattern.namespace else namespace_prefix
            named_urls.extend(extract_named_urls(pattern, sub_namespace))

    return named_urls
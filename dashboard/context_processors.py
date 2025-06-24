from .models import Quicklinks, ContactInfo, SocialLinks, MenuItem
from .utils import get_all_models

def global_context(request):
    menu_items = MenuItem.objects.filter(parent=None).prefetch_related('children').order_by('order')
    quick_links = Quicklinks.objects.all()
    contact_infos = ContactInfo.objects.all()
    social_links = SocialLinks.objects.all()
    raw_models = get_all_models()

    models = [
        (name, {
            'class': model,
            'verbose_name': model._meta.verbose_name_plural.title()
        }) for name, model in raw_models.items()
    ]

    return {
        'menu_items': menu_items,
        'quick_links': quick_links,
        'contact_infos': contact_infos,
        'social_links': social_links,
        'models': models,
    }

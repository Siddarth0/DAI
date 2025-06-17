from .models import Quicklinks, ContactInfo, SocialLinks, MenuItem

def menu_items_context(request):
    items = MenuItem.objects.filter(parent=None).prefetch_related('children').order_by('order')
    return {
        'menu_items': items
        }

def quick_links(request):
    return {
        'quick_links': Quicklinks.objects.all()
    }

def contact_infos(request):
    return{
        'contact_infos': ContactInfo.objects.all()
    }

def social_links(request):
    return{
        'social_links': SocialLinks.objects.all
    }

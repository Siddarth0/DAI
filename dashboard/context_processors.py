from .models import NavBar, Quicklinks, ContactInfo

def navbar_content(request):
    return {
        'navbar_content': NavBar.objects.all()
    }

def quick_links(request):
    return {
        'quick_links': Quicklinks.objects.all()
    }

def contact_infos(request):
    return{
        'contact_infos': ContactInfo.objects.all()
    }

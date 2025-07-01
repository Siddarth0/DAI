from dashboard.utils import extract_named_urls


MENU_TYPE_CHOICES = [
    ('internal', 'Internal Page (by named URL)'),
    ('external', 'External URL'),
    ('cms', 'CMS Page'),
]

def get_internal_url_choices():
    """Returns a list of internal named URL choices for menu linking."""
    return [('', 'Select Internal Route')] + extract_named_urls()

def get_cms_page_choices():
    from dashboard.models import CMSPage
    """Returns a list of CMS page choices for menu linking."""
    return [('', 'Select CMS Page')] + [
        (page.id, page.title) for page in CMSPage.objects.all()
    ]

CATEGORY_CHOICES = [
        ('news', 'News'),
        ('webinar', 'Webinar'),
        ('event', 'Event'),
        # Add more categories as needed
    ]
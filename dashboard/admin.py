from django.contrib import admin
from .models import NavBar, Banner, SMEStep, Service, Guidelines, NewsEvent, ContactInfo, Quicklinks, SocialLinks

@admin.register(NavBar)
class NavBarAdmin(admin.ModelAdmin):
    list_display=('name', 'url')

    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'button1_text','button1_link', 'button2_text','button2_link','order')
    ordering = ['order']

    
@admin.register(SMEStep)
class SMEStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'order')
    ordering = ('order',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon','subtitle','title','description','order')
    ordering = ('order',)

@admin.register(Guidelines)
class Guidelines(admin.ModelAdmin):
    list_display = ('icon','title','description','order')
    ordering = ('order',)

@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_webinar', 'start_date', 'end_date')
    list_filter = ('is_webinar', 'start_date', 'end_date', 'created_at')
    ordering = ('-start_date',)

    exclude = ('created_at', 'updated_at')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'value')

@admin.register(Quicklinks)
class QuicklinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('icon', 'url')

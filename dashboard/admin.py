from django.contrib import admin
from django import forms
from django.urls import get_resolver, reverse
from .models import MenuItem, Banner, SMEStep, Service, Guidelines, NewsEvent, ContactInfo, Quicklinks, SocialLinks, Notice, CMSPage
from .forms import MenuItemAdminForm, CMSPageAdminForm


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    readonly_fields = ['module']

    class Media:
        js = ('admin/menuitem_type_toggle.js',)

    list_display = ('name', 'type', 'module', 'order', 'parent')
    list_filter = ('type', 'parent')

    
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
    list_display = ('title', 'category', 'start_date', 'end_date')
    list_filter = ('category', 'start_date', 'end_date', 'created_at')
    ordering = ('-start_date',)

    readonly_fields = ('created_at', 'updated_at')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'value')

@admin.register(Quicklinks)
class QuicklinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ('icon', 'url')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'image','pdf','is_popup', 'popup_order','created_at')
    list_editable = ('is_popup', 'popup_order')
    ordering = ('popup_order','-created_at',)


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    form = CMSPageAdminForm
    readonly_fields = ['slug'] 
    list_display = ['title', 'slug', 'updated_at']

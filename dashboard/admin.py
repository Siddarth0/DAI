from django.contrib import admin
from django import forms
from django.urls import get_resolver
from .models import MenuItem, Banner, SMEStep, Service, Guidelines, NewsEvent, ContactInfo, Quicklinks, SocialLinks, Notice, CMSPage


class MenuItemAdminForm(forms.ModelForm):
    internal_link = forms.ChoiceField(
        choices=[],
        required=False,
        label='Internal Link'
    )
    cms_link = forms.ChoiceField(
        choices=[],
        required=False,
        label='CMS Page'
    )
    external_link = forms.CharField(
        required=False,
        label='External URL'
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'type', 'internal_link', 'cms_link', 'external_link', 'order', 'parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        url_patterns = get_resolver().reverse_dict
        internal_choices = [('#', '# (No Link / Stay on Same Page)')] + [(name, name) for name in url_patterns if isinstance(name, str) and not name.startswith("admin")]
        cms_choices = [('#', '# (No Link / Stay on Same Page)')] + [(page.slug, page.title) for page in CMSPage.objects.all()]

        self.fields['internal_link'].choices = [('', 'Select Internal URL')] + internal_choices
        self.fields['cms_link'].choices = [('', 'Select CMS Page')] + cms_choices

        # Set initial value for the correct link field based on instance type and link
        if self.instance and self.instance.pk:
            if self.instance.type == 'internal':
                self.initial['internal_link'] = self.instance.link
            elif self.instance.type == 'cms':
                self.initial['cms_link'] = self.instance.link
            elif self.instance.type == 'external':
                self.initial['external_link'] = self.instance.link

    def clean(self):
        cleaned_data = super().clean()
        link_type = cleaned_data.get('type')

        if link_type == 'internal':
            cleaned_data['link'] = cleaned_data.get('internal_link') or '#'
        elif link_type == 'cms':
            cleaned_data['link'] = cleaned_data.get('cms_link') or '#'
        elif link_type == 'external':
            cleaned_data['link'] = cleaned_data.get('external_link') or '#'
        else:
            cleaned_data['link'] = '#'

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        link_type = self.cleaned_data.get('type')
        if link_type == 'internal':
            instance.link = self.cleaned_data.get('internal_link') or '#'
        elif link_type == 'cms':
            instance.link = self.cleaned_data.get('cms_link') or '#'
        elif link_type == 'external':
            instance.link = self.cleaned_data.get('external_link') or '#'
        else:
            instance.link = '#'

        if commit:
            instance.save()
        return instance



@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm

    class Media:
        js = ('admin/menuitem_type_toggle.js',)

    list_display = ('name', 'type', 'link', 'order', 'parent')
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
    list_display = ('title', 'is_webinar', 'start_date', 'end_date')
    list_filter = ('is_webinar', 'start_date', 'end_date', 'created_at')
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
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created_at')
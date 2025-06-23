from django import forms
from .utils import extract_named_urls
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

        internal_choices = [('', 'Select Internal Route')] + extract_named_urls()
        self.fields['internal_link'].choices = internal_choices


        cms_choices = [('', 'Select CMS Page')] + [(page.id, page.title) for page in CMSPage.objects.all()]
        self.fields['cms_link'].choices = cms_choices


        # Ensuring initial value for the correct link field based on instance type and link
        if self.instance and self.instance.pk:
            selected_type = self.instance.type

            if selected_type == 'internal':
                self.initial['module'] = self.instance.module
            elif selected_type == 'cms':
                self.initial['cms_link'] = self.instance.cms_id.id if self.instance.cms_id else None 
            elif selected_type == 'external':
                self.initial['external_link'] = self.instance.module


    def clean(self):
        cleaned_data = super().clean()
        link_type = cleaned_data.get('type')

        # Validate link type explicitly
        if link_type not in ['internal', 'cms', 'external']:
            raise forms.ValidationError("Invalid link type selected.")

        # Dynamically set link field based on type
        if link_type == 'cms':
            cleaned_data['cms_id'] = CMSPage.objects.get(id=cleaned_data.get('cms_link'))

        elif link_type == 'internal':
            cleaned_data['module'] = cleaned_data.get('internal_link')

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        link_type = self.cleaned_data.get('type')

        if link_type == 'cms':
            instance.cms_id = self.cleaned_data.get('cms_id') # Save the selected CMSPage


        elif link_type == 'internal':
            instance.module = self.cleaned_data.get('module')  # Store named route

        elif link_type == 'external':
            instance.module = self.cleaned_data.get('external_link')

        if commit:
            instance.save()
        return instance

class BannerAdminForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'


class SMEStepAdminForm(forms.ModelForm):
    class Meta:
        model = SMEStep
        fields = '__all__'


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class GuidelinesAdminForm(forms.ModelForm):
    class Meta:
        model = Guidelines
        fields = '__all__'


class NewsEventAdminForm(forms.ModelForm):
    class Meta:
        model = NewsEvent
        exclude = ['created_at', 'updated_at']


class ContactInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class QuicklinksAdminForm(forms.ModelForm):
    class Meta:
        model = Quicklinks
        fields = '__all__'


class SocialLinksAdminForm(forms.ModelForm):
    class Meta:
        model = SocialLinks
        fields = '__all__'


class NoticeAdminForm(forms.ModelForm):
    class Meta:
        model = Notice
        exclude = ['created_at']


class CMSPageAdminForm(forms.ModelForm):
    class Meta:
        model = CMSPage
        exclude = ['slug', 'created_at', 'updated_at']


FORM_MAP = {
    'menuitem': MenuItemAdminForm,
    'banner': BannerAdminForm,
    'smestep': SMEStepAdminForm,
    'service': ServiceAdminForm,
    'guidelines': GuidelinesAdminForm,
    'newsevent': NewsEventAdminForm,
    'contactinfo': ContactInfoAdminForm,
    'quicklinks': QuicklinksAdminForm,
    'sociallinks': SocialLinksAdminForm,
    'notice': NoticeAdminForm,
    'cmspage': CMSPageAdminForm,
}
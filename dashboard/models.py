from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.urls import NoReverseMatch

import datetime


class MenuItem(models.Model):
    MENU_TYPE_CHOICES = [
        ('internal', 'Internal Page (by named URL)'),
        ('external', 'External URL'),
        ('cms', 'CMS Page'),
    ]


    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=MENU_TYPE_CHOICES, default='internal')
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    cms_id = models.ForeignKey('CMSPage', on_delete=models.SET_NULL, null=True, blank=True)
    module = models.CharField(max_length=100, blank=True, null=True, help_text="Named URL for internal pages")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the actual URL this menu item should point to."""
        try:
           if self.type == 'internal' and self.module:
               return reverse(self.module)
            
           elif self.type == 'cms' and self.cms_id:
               return reverse("cms_page_detail", kwargs={"slug": self.cms_id.slug})
           elif self.type == 'external' and self.module:
               return self.module 
        except NoReverseMatch:
            pass #

        return '#'

    

class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    button1_text = models.CharField(max_length=50, blank=True, null=True)
    button1_link = models.URLField(blank=True, null=True)

    button2_text = models.CharField(max_length=50, blank=True, null=True)
    button2_link = models.URLField(blank=True, null=True)


    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.title}"
    

    
class SMEStep(models.Model):
    icon = models.ImageField(upload_to='static/images/icons/') 
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0, help_text="Order in which the steps appear")

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Service(models.Model):
    tag = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    icon = models.FileField(upload_to='static/images/icons/')
    order = models.PositiveIntegerField(default=0, help_text='Order in which the services appear')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
class Guidelines(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.FileField(upload_to='static/images/icons/')
    order = models.PositiveIntegerField(default=0, help_text='Order in which the services appear')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class NewsEvent(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='static/images/newspics/')
    is_webinar = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class ContactInfo(models.Model):
    type_choices = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('location', 'Location'),
    ]

    contact_type = models.CharField(max_length=10, choices=type_choices)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"
    

class Quicklinks(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class SocialLinks(models.Model):
    icon = models.FileField(upload_to='static/images/icons/')
    url= models.URLField()

    def __str__(self):
        return "SocialLinks"
    
class Notice(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/notices/', blank=True, null=True)
    pdf = models.FileField(upload_to='static/notices',blank=True, null=True)
    is_popup = models.BooleanField(default=False, help_text="Check to show this notice as a pop up")
    popup_order = models.PositiveIntegerField(blank = True, null=True, help_text="order of popup display if multiple") 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('notice_detail', kwargs={"id": self.id})
    
    
    class Meta:
        ordering = ['popup_order', '-created_at']


class CMSPage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, editable=False)
    content = models.TextField()
    meta_tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for SEO")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's missing
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while CMSPage.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug  # Set the unique slug once
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cms_page_detail", kwargs={"slug": self.slug})


    

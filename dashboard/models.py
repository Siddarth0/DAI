from django.db import models
from django.utils import timezone
import datetime

class NavBar(models.Model):
    home_link = models.CharField(max_length=50, default='Home')
    about_link = models.CharField(max_length=100, default='About')
    schemes_link = models.CharField(max_length=50, default='Schemes')
    policies_link = models.CharField(max_length=50, default='Policies')
    contact_link = models.CharField(max_length=50, default='Contact')
    navbar_register = models.CharField(max_length=50, default='Register')
    navbar_login = models.CharField(max_length=50, default='Login')

    def __str__(self):
        return "Nav Bar Content"

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
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
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

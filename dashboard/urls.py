from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:id>/', views.notice_detail, name = 'notice_detail'),
]
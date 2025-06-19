from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:id>/', views.notice_detail, name = 'notice_detail'),

    path('services/', views.service_list, name='service_list'),
    path('services/<int:id>/', views.service_detail, name='service_detail'),

    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),

    path('cms/<slug:slug>/', views.cms_page_detail, name='cms_page_detail'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
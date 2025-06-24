from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Public / Landing page routes
    path('', views.landing_page, name='landing_page'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:id>/', views.notice_detail, name='notice_detail'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:id>/', views.service_detail, name='service_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('cms/<slug:slug>/', views.cms_page_detail, name='cms_page_detail'),

    # Admin Dashboard routes
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/<str:model_name>/', views.model_list, name='model_list'),
    path('dashboard/<str:model_name>/add/', views.model_add, name='model_add'),
    path('dashboard/<str:model_name>/<int:pk>/edit/', views.model_edit, name='model_edit'),
    path('dashboard/<str:model_name>/<int:pk>/delete/', views.model_delete, name='model_delete'),

    # Auth routes (Login/Logout)
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Register
    path('welcomePage/', views.welcome_page, name='welcome_page'),
]

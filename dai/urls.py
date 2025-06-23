from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace = 'dashboard')), 
    path('admin-dashboard/', include(('adminDashboard.urls', 'adminDashboard'), namespace='adminDashboard')),
    path('auth/', include(('authys.urls', 'authys'), namespace='authys')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
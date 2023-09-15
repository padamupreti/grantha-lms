from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from authentication.views import login_or_register

urlpatterns = [
    path('', login_or_register, name='login-or-register'),
    path('auth/', include('authentication.urls')),
    path('', include('dashboard.urls')),
    path('qr/', include('qrmanager.urls')),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

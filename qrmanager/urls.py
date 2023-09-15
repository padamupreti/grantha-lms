from django.urls import path

from .views import download_qr, upload_qr

app_name = 'qrmanager'
urlpatterns = [
    path('download/', download_qr, name='download-qr'),
    path('upload/', upload_qr, name='upload-qr')
]

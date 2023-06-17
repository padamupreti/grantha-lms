from django.urls import path

from .views import login_or_register, register_librarian, register_member, login_user

app_name = 'authentication'
urlpatterns = [
    path('', login_or_register, name='login-or-register'),
    path('register-librarian/', register_librarian, name='register-librarian'),
    path('register-member/', register_member, name='register-member'),
    path('login/', login_user, name='login'),
]

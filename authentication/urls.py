from django.urls import path

from .views import (register_librarian, register_member,
                    login_user, logout_user)

app_name = 'authentication'
urlpatterns = [
    path('register-librarian/', register_librarian, name='register-librarian'),
    path('register-member/', register_member, name='register-member'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='authentication:login-or-register')
def home(request):
    return render(request, 'dashboard/home.html', {})

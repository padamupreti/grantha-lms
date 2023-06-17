from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from .forms import LMSUserCreationForm


def login_or_register(request):
    return render(request, 'authentication/login_or_register.html', {})


def register_user(request, is_librarian):
    form = LMSUserCreationForm(request.POST or None)
    user_type = 'Librarian' if is_librarian else 'Member'
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_librarian = is_librarian
            new_user.save()
            # return redirect('dashboard:home') TODO
    return render(request, 'authentication/register.html', {'form': form, 'user_type': user_type})


def register_librarian(request):
    return register_user(request, True)


def register_member(request):
    return register_user(request, False)


def login_user(request):
    form = AuthenticationForm(request.POST or None)
    return render(request, 'authentication/login.html', {'form': form})

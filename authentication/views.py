from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import LMSUserCreationForm


def login_or_register(request):
    return render(request, 'authentication/login_or_register.html', {})


def register_user(request, is_librarian):
    form = LMSUserCreationForm(request.POST or None)
    context = {
        'form': form,
        'user_type': 'Librarian' if is_librarian else 'Member'
    }
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_librarian = is_librarian
            new_user.save()
            login(request, new_user)
            # TODO to modify to redirect to dashboard
            return redirect('authentication:login-or-register')
    return render(request, 'authentication/register.html', context)


def register_librarian(request):
    return register_user(request, True)


def register_member(request):
    return register_user(request, False)


def login_user(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # TODO to modify to redirect to dashboard
                return redirect('authentication:login-or-register')
    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('authentication:login-or-register')

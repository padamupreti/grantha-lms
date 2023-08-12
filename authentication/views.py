from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .decorators import redirect_authenticated
from .forms import LMSUserCreationForm


@redirect_authenticated
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
            return redirect('dashboard:home')
    return render(request, 'authentication/register.html', context)


@redirect_authenticated
def register_librarian(request):
    return register_user(request, True)


@redirect_authenticated
def register_member(request):
    return register_user(request, False)


@redirect_authenticated
def login_user(request):
    form = AuthenticationForm(data=request.POST or None)
    redirect_url = request.GET.get('next') or 'dashboard:home'
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(redirect_url)
    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login-or-register')

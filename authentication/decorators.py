from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def redirect_authenticated(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return func(request, *args, **kwargs)

    return inner


def only_librarians(func):
    def inner(request, *args, **kwargs):
        if not request.user.is_librarian:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return inner


def only_members(func):
    def inner(request, *args, **kwargs):
        if request.user.is_librarian:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return inner

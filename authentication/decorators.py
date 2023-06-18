from django.shortcuts import redirect


def redirect_authenticated(func):
    def inner(request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return func(request)

    return inner

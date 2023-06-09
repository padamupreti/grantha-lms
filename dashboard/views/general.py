from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.contrib.auth.decorators import login_required


@login_required(login_url='authentication:login-or-register')
def home(request):
    return render(request, 'dashboard/home.html', {})


class LibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_librarian


class MemberView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_librarian

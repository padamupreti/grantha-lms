from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from ..models import Author, Publisher, Category, Book, Issue, Request


@login_required(login_url='authentication:login-or-register')
def home(request):
    books = Book.objects.count()
    if request.user.is_librarian:
        context = {
            'books': books,
            'issues': Issue.objects.count(),
            'book_requests': Request.objects.filter(is_fulfilled=False).count()
        }
    else:
        context = {
            'books': books,
            'authors': Author.objects.count(),
            'publishers': Publisher.objects.count(),
            'categories': Category.objects.count()
        }
    return render(request, 'dashboard/home.html', context)


class LibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_librarian


class MemberView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_librarian

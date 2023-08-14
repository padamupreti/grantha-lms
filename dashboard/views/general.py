from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View

from datetime import date

from ..models import Book, BookCopy, Issue, Request, LateFine


def home(request):
    template_name = 'dashboard/member_home.html'
    context = {}

    if not request.user.is_anonymous and request.user.is_librarian:
        template_name = 'dashboard/librarian_home.html'
    elif not request.user.is_anonymous and not request.user.is_librarian:
        books = Book.objects.all()
        all_titles = books.count()
        available_titles = 0
        for book in books:
            available_copies = BookCopy.objects.filter(
                book=book, is_available=True).count()
            if available_copies > 0:
                available_titles += 1

        issues = Issue.objects.filter(
            member=request.user, returned_date=None).order_by('due_date')
        for issue in issues:
            issue.is_due = False
            if issue.due_date <= date.today():
                issue.is_due = True

        requests = Request.objects.filter(
            member=request.user, is_fulfilled=False)

        late_fines = LateFine.objects.filter(member=request.user)

        context = {
            'all_titles': all_titles,
            'available_titles': available_titles,
            'issues': issues,
            'requests': requests,
            'late_fines': late_fines
        }

    return render(request, template_name, context)


class LibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_librarian


class MemberView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_librarian

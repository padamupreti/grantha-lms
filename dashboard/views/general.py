from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View

from datetime import date

from ..models import Book, BookCopy, Issue, Request, LateFine


def home(request):
    # TODO manage shared logic in a module for member home and librarian home
    if not request.user.is_authenticated:
        return redirect('dashboard:list-books')

    template_name = 'dashboard/member_home.html'

    books = Book.objects.all()
    all_titles = books.count()
    available_titles = 0
    for book in books:
        available_copies = BookCopy.objects.filter(
            book=book, is_available=True).count()
        if available_copies > 0:
            available_titles += 1

    context = {
        'all_titles': all_titles,
        'available_titles': available_titles
    }

    if not request.user.is_anonymous and request.user.is_librarian:
        template_name = 'dashboard/librarian_home.html'
        pending_requests = Request.objects.filter(
            is_fulfilled=False).order_by('request_date')
        current_issues = Issue.objects.filter(
            returned_date=None).order_by('returned_date')

        for issue in current_issues:
            issue.is_due = False
            if issue.due_date <= date.today() and issue.returned_date is None:
                issue.is_due = True

        overdue_count = current_issues.filter(
            due_date__lte=date.today()).count()

        context.update({
            'issues_count': current_issues.count(),
            'overdue_count': overdue_count,
            'issues': current_issues[:5],
            'pending_requests_count': pending_requests.count(),
            'pending_requests': pending_requests[:5]
        })

    elif not request.user.is_anonymous and not request.user.is_librarian:
        issues = Issue.objects.filter(
            member=request.user, returned_date=None).order_by('returned_date')
        for issue in issues:
            issue.is_due = False
            if issue.due_date <= date.today() and issue.returned_date is None:
                issue.is_due = True

        overdue_count = issues.filter(
            due_date__lte=date.today()).count()

        requests = Request.objects.filter(
            member=request.user, is_fulfilled=False)
        late_fines = LateFine.objects.filter(
            member=request.user).order_by('-fined_date')

        context.update({
            'issues': issues,
            'overdue_count': overdue_count,
            'requests': requests,
            'late_fines': late_fines
        })

    return render(request, template_name, context)


class LibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_librarian

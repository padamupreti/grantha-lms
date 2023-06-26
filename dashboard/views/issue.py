from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import date

from ..models import BookCopy, Issue
from ..forms.issue_forms import IssueCreateForm


@login_required
def issue_book(request):
    form = IssueCreateForm(request.POST or None)
    context = {
        'form': form,
        'item_type': 'Issue'
    }
    if request.method == 'POST':
        if form.is_valid():
            form.create()
            return redirect('dashboard:list-issues')
    return render(request, 'dashboard/generic_edit.html', context)


@login_required
def list_issues(request):
    copies_to_return = list(BookCopy.objects.filter(is_available=False))
    copies_returned = list(BookCopy.objects.filter(is_available=True))
    context = {
        'issues_to_return': Issue.objects.filter(book_copy__in=copies_to_return),
        'issues_returned': Issue.objects.filter(book_copy__in=copies_returned)
    }
    return render(request, 'dashboard/list_issues.html', context)


@login_required
def return_issued_book(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    context = {
        'book': issue.book_copy.book,
        'member': issue.member,
    }
    if request.method == 'POST':
        issue.book_copy.is_available = True
        issue.book_copy.save()
        issue.returned_date = date.today()
        issue.save()
        return redirect('dashboard:list-issues')
    return render(request, 'dashboard/return_issued.html', context)

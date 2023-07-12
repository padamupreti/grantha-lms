from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import date

from ..models import BookCopy, Issue, LateFine
from ..forms.issue_forms import IssueCreateForm


PER_DAY_FINE = 1


@login_required
def issue_book(request):
    form = IssueCreateForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.create()
            return redirect('dashboard:list-issues')
    return render(request, 'dashboard/create_issue.html', context)


@login_required
def list_issues(request):
    context = {
        'issues_to_return': Issue.objects.filter(returned_date=None),
        'issues_returned': Issue.objects.exclude(returned_date=None)
    }
    return render(request, 'dashboard/list_issues.html', context)


@login_required
def return_issued_book(request, pk):
    issue = get_object_or_404(Issue, id=pk)
    due_days = None
    due_date = issue.due_date
    today = date.today()
    if due_date > today:
        message = 'Book is not due for submission'
    else:
        due_days = abs(today - due_date).days
        if due_days == 0:
            message = 'Book is due for submission today'
        else:
            fine_amount = due_days * PER_DAY_FINE
            message = f'Book is late for submission by {due_days} day(s). Late fine amount: Rupees {fine_amount}'
    context = {
        'book': issue.book_copy.book,
        'member': issue.member,
        'message': message,
        'due_days': due_days
    }
    if request.method == 'POST':
        if due_days:
            LateFine.objects.create(
                book_copy=issue.book_copy,
                member=issue.member,
                late_days=due_days,
                amount=fine_amount,
                fined_date=today
            )
        issue.book_copy.is_available = True
        issue.book_copy.save()
        issue.returned_date = today
        issue.save()
        return redirect('dashboard:list-issues')
    return render(request, 'dashboard/return_issued.html', context)

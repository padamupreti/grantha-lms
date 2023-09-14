from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from datetime import date

from authentication.decorators import only_librarians

from ..models import BookCopy, Issue, LateFine, Request
from ..forms.issue_forms import IssueCreateForm


@login_required
@only_librarians
def issue_book(request):
    book_request = None
    book_request_id = request.GET.get('rid', None)
    if book_request_id:
        book_request = Request.objects.get(id=book_request_id)
    if request.method == 'GET':
        form = IssueCreateForm(
            initial={
                'book': book_request.book,
                'member': book_request.member
            }
        ) if book_request else IssueCreateForm()
    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            form.create()
            if book_request:
                book_request.is_fulfilled = True
                book_request.save()
            return redirect('dashboard:list-issues')
    return render(request, 'dashboard/create_issue.html', {'form': form})


@login_required
@only_librarians
def list_issues(request):
    # TODO manage in module shared between member report and member home
    issues = Issue.objects.order_by('returned_date')
    for issue in issues:
        issue.is_due = False
        if issue.due_date <= date.today() and issue.returned_date is None:
            issue.is_due = True

    return render(request, 'dashboard/list_issues.html', {'issues': issues})


@login_required
@only_librarians
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
            fine_amount = due_days * issue.late_fine_rate
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

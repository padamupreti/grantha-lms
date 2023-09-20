from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import date

from authentication.decorators import only_librarians

from ..models import Issue, LateFine, Request
from ..forms.issue_forms import IssueCreateForm
from ..utils import add_is_due


@login_required
@only_librarians
def issue_book(request):
    book_request = None
    book_request_id = request.GET.get('rid', None)
    if book_request_id:
        qs = Request.objects.filter(is_fulfilled=False)
        try:
            book_request = get_object_or_404(qs, id=book_request_id)
        except ValueError:
            messages.error(request, f'Invalid rid {book_request_id}.')
            return redirect('dashboard:list-issues')

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
    query_params = request.GET
    p_title = query_params.get('query')

    issues = Issue.objects.order_by('returned_date')
    if p_title:
        issues = issues.filter(book_copy__book__title__icontains=p_title)

    add_is_due(issues)

    context = {
        'issues': issues,
        'search_placeholder': 'Search by book title',
        'query_text': p_title
    }

    return render(request, 'dashboard/list_issues.html', context)


@login_required
@only_librarians
def return_issued_book(request, pk):
    issue = get_object_or_404(Issue, id=pk)

    if issue.returned_date:
        messages.warning(request, 'Issue has already been returned prior.')
        return redirect('dashboard:list-issues')

    due_days = 0
    fine_amount = 0
    due_date = issue.due_date
    today = date.today()
    if due_date > today:
        status = 'Not due'
    else:
        due_days = abs(today - due_date).days
        if due_days == 0:
            status = 'Due Today'
        else:
            fine_amount = due_days * issue.late_fine_rate
            status = 'Overdue'

    context = {
        'issue': issue,
        'status': status,
        'due_days': due_days,
        'fine_amount': fine_amount
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

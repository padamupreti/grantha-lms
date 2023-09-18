from datetime import date

from qrmanager import get_encoded_member_qr

from .models import Issue, Request, LateFine


def has_pending_requests(member, book):
    unfulfilled_requests = Request.objects.filter(
        member=member, book=book, is_fulfilled=False)
    if unfulfilled_requests:
        return True
    return False


def has_active_requests(book):
    book_requests = Request.objects.filter(book=book, is_fulfilled=False)
    if book_requests:
        return True
    return False


def get_member_context(request, member):
    encoded_qr = get_encoded_member_qr(request.get_host(), member)

    issues = Issue.objects.filter(
        member=member).order_by('returned_date')
    for issue in issues:
        issue.is_due = False
        if issue.due_date <= date.today() and issue.returned_date is None:
            issue.is_due = True

    requests = Request.objects.filter(member=member).order_by('is_fulfilled')
    late_fines = LateFine.objects.filter(member=member).order_by('-fined_date')

    context = {
        'encoded_qr': encoded_qr,
        'member': member,
        'issues': issues,
        'requests': requests,
        'late_fines': late_fines
    }

    return context

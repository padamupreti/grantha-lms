from datetime import date

from qrmanager import get_encoded_member_qr

from .models import Issue, Request, LateFine, BookCopy, BookAuthor


def add_is_due(issues):
    for issue in issues:
        issue.is_due = False
        if issue.due_date < date.today() and issue.returned_date is None:
            issue.is_due = True


def has_pending_requests(book, member=None):
    pending_requests = Request.objects.filter(book=book, is_fulfilled=False)
    if member:
        pending_requests = pending_requests.filter(member=member)
    if pending_requests:
        return True
    return False


def add_book_attributes(book, request):
    all_copies = BookCopy.objects.filter(book=book)
    book.all_copies = all_copies.count()
    book.available_copies = all_copies.filter(is_available=True).count()

    book_author_rels = BookAuthor.objects.filter(
        book=book).select_related('author')
    ba_rel = book_author_rels.first()
    book.author = ba_rel.author if ba_rel is not None else None
    book.multi_a = True if book_author_rels.count() > 1 else False

    book.is_requested = False
    if request.user.is_authenticated:
        book.is_requested = has_pending_requests(book, request.user)


def get_member_context(request, member):
    encoded_qr = get_encoded_member_qr(request.get_host(), member)

    issues = Issue.objects.filter(
        member=member).order_by('due_date')
    add_is_due(issues)
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

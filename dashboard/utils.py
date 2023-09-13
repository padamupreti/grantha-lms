from .models import Request


def has_pending_requests(member, book):
    unfulfilled_requests = Request.objects.filter(
        member=member, book=book, is_fulfilled=False)
    if unfulfilled_requests:
        return True
    return False

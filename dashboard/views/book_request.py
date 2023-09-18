from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import date

from authentication.decorators import only_members, only_librarians

from ..models import Book, Request, BookCopy
from ..utils import has_pending_requests


@login_required
@only_members
def request_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    is_available = len(BookCopy.objects.filter(
        book=book, is_available=True)) > 0
    if request.method == 'POST':
        pending = has_pending_requests(request.user, book)
        if not is_available:
            messages.danger(
                request, f'Book "{book}" is not available in Library.')
        elif pending:
            messages.warning(
                request, f'Request for book "{book}" is already pending.')
        else:
            Request.objects.create(
                book=book, member=request.user, request_date=date.today(), is_fulfilled=False)
            messages.success(request, f'Book "{book}" requested successfully!')
        return redirect('dashboard:list-books')

    context = {
        'book': book,
        'is_available': is_available
    }

    return render(request, 'dashboard/request_book.html', context)


@login_required
@only_librarians
def list_book_requests(request):
    query_params = request.GET
    p_title = query_params.get('query')

    book_requests = Request.objects.order_by('is_fulfilled')
    if p_title:
        book_requests = book_requests.filter(book__title__icontains=p_title)

    context = {
        'object_list': book_requests,
        'search_placeholder': 'Search by book title',
        'query_text': p_title
    }

    return render(request, 'dashboard/list_book_requests.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from datetime import date

from authentication.decorators import only_members, only_librarians

from .general import LibrarianView
from ..models import Book, Request, BookCopy


@login_required
@only_members
def request_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    is_available = len(BookCopy.objects.filter(
        book=book, is_available=True)) > 0
    if request.method == 'POST':
        if is_available:
            Request.objects.create(
                book=book, member=request.user, request_date=date.today(), is_fulfilled=False)
        return redirect('dashboard:book-detail', pk)
    context = {
        'book': book,
        'is_available': is_available
    }
    return render(request, 'dashboard/request_book.html', context)


class BookRequestList(LoginRequiredMixin, LibrarianView, ListView):
    model = Request
    template_name = 'dashboard/list_book_requests.html'

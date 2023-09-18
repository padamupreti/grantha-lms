from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import ProtectedError

from authentication.decorators import only_librarians

from ..models import Author, Book, BookAuthor, BookCategory, BookCopy
from ..forms.book_forms import BookCreateForm, BookUpdateForm
from ..utils import has_pending_requests, has_active_requests


@login_required
@only_librarians
def create_book(request):
    form = BookCreateForm(request.POST or None)
    context = {
        'form': form,
        'item_type': 'Book'
    }
    if request.method == 'POST':
        if form.is_valid():
            form.create()
            return redirect('dashboard:list-books')
    return render(request, 'dashboard/generic_edit.html', context)


def list_books(request):
    # Get various search parameters as query parameters
    query_params = request.GET
    p_filter = query_params.get('filter')
    p_query = query_params.get('query')

    # Filter results from queryset according to search parameters
    qs = Book.objects.all()
    if p_filter and p_query:
        if p_filter == 'title':
            qs = qs.filter(title__icontains=p_query)
        if p_filter == 'publisher' and len(qs) > 0:
            qs = qs.filter(publisher__name__icontains=p_query)
        if p_filter == 'isbn' and len(qs) > 0:
            qs = qs.filter(isbn__exact=p_query)
        if p_filter == 'author' and len(qs) > 0:
            book_author_rels = BookAuthor.objects.filter(
                author__name__icontains=p_query)
            titles = [ba.book.title for ba in book_author_rels]
            qs = qs.filter(title__in=titles)
        if p_filter == 'category' and len(qs) > 0:
            book_category_rels = BookCategory.objects.filter(
                category__name__icontains=p_query)
            titles = [bc.book.title for bc in book_category_rels]
            qs = qs.filter(title__in=titles)

    # Add additional attributes to books in queryset
    books = []
    for book in qs:
        book_author_rels = BookAuthor.objects.filter(
            book=book).select_related('author')
        # TODO (and also all associated fixes for nullable fields for every model)
        ba_rel = book_author_rels.first()
        book.author = ba_rel.author if ba_rel is not None else None
        book.multi_authors = True if book_author_rels.count() > 1 else False
        book.is_requested = False
        if request.user.is_authenticated:
            book.is_requested = has_pending_requests(request.user, book)
        all_copies = BookCopy.objects.filter(book=book)
        book.all_copies = all_copies.count()
        book.available_copies = all_copies.filter(is_available=True).count()
        books.append(book)

    context = {
        'books': books,
        'p_filter': p_filter,
        'p_query': p_query,
    }

    return render(request, 'dashboard/list_books.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    book_author_rels = BookAuthor.objects.filter(
        book=book).select_related('author')
    book_category_rels = BookCategory.objects.filter(
        book=book).select_related('category')
    is_requested = False
    if request.user.is_authenticated:
        is_requested = has_pending_requests(request.user, book)
    is_available = len(BookCopy.objects.filter(
        book=book, is_available=True)) > 0
    context = {
        'book': book,
        'is_requested': is_requested,
        'is_available': is_available,
        'authors': [ba.author.name for ba in book_author_rels],
        'categories': [bc.category.name for bc in book_category_rels],
    }
    return render(request, 'dashboard/book_detail.html', context)


@login_required
@only_librarians
def update_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book_author_rels = BookAuthor.objects.select_related(
        'author').filter(book=book)
    book_category_rels = BookCategory.objects.select_related(
        'category').filter(book=book)
    form = BookUpdateForm(
        request.POST or None, book=book,
        book_author_rels=book_author_rels, book_category_rels=book_category_rels,
        initial={
            'title': book.title,
            'quantity': BookCopy.objects.filter(book=book).count(),
            'isbn': book.isbn,
            'authors': [ba.author for ba in book_author_rels],
            'publisher': book.publisher,
            'categories': [bc.category for bc in book_category_rels]
        })
    context = {
        'form': form,
        'item_type': 'Book'
    }
    if request.method == 'POST':
        if form.is_valid():
            if form.has_changed():
                form.update()
            return redirect('dashboard:list-books')
    return render(request, 'dashboard/generic_edit.html', context)


@login_required
@only_librarians
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        if has_active_requests(book):
            messages.warning(
                request, f'Book "{book}" cannot have active requests for successful deletion.')
            return redirect('dashboard:list-books')
        try:
            book.delete()
            # TODO use messages framework to display message after successful actions
            # creation, update and deletion of various items
            messages.success(request, f'Book "{book}" deleted successfully!')
            return redirect(reverse_lazy('dashboard:list-books'))
        except ProtectedError:
            messages.warning(
                request, f'Book "{book}" cannot have any copies for successful deletion.')
            return redirect('dashboard:list-books')

    context = {
        'item_type': 'Book',
        'object': book
    }

    return render(request, 'dashboard/generic_delete.html', context)

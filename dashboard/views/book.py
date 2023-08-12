from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from authentication.decorators import only_librarians

from .general import LibrarianView
from ..models import Author, Book, BookAuthor, BookCategory, BookCopy
from ..forms.book_forms import BookCreateForm, BookUpdateForm
from ..mixins import DeleteMixin


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
    p_author = query_params.get('author')
    p_publisher = query_params.get('publisher')
    p_category = query_params.get('category')

    # Filter results from queryset according to search parameters
    qs = Book.objects.all()
    if p_publisher:
        qs = qs.filter(publisher__name__icontains=p_publisher)
    if p_author and len(qs) > 0:
        book_author_rels = BookAuthor.objects.filter(
            author__name__icontains=p_author)
        titles = [ba.book.title for ba in book_author_rels]
        qs = qs.filter(title__in=titles)
    if p_category and len(qs) > 0:
        book_category_rels = BookCategory.objects.filter(
            category__name__icontains=p_category)
        titles = [bc.book.title for bc in book_category_rels]
        qs = qs.filter(title__in=titles)

    # Add additional attributes to books in queryset
    books = []
    for book in qs:
        book_author_rels = BookAuthor.objects.filter(
            book=book).select_related('author')
        book.author = book_author_rels.first().author
        book.multi_authors = True if book_author_rels.count() > 1 else False
        books.append(book)

    return render(request, 'dashboard/list_books.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    book_author_rels = BookAuthor.objects.filter(
        book=book).select_related('author')
    book_category_rels = BookCategory.objects.filter(
        book=book).select_related('category')
    is_available = len(BookCopy.objects.filter(
        book=book, is_available=True)) > 0
    context = {
        'book': book,
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


class BookDeleteView(DeleteMixin, LibrarianView):
    model = Book
    success_url = reverse_lazy('dashboard:list-books')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Book', **kwargs)

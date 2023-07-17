from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from authentication.decorators import only_librarians

from .general import LibrarianView
from ..models import Book, BookAuthor, BookCategory, BookCopy
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


@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'dashboard/list_books.html', {'books': books})


@login_required
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

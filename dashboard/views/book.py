from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ..models import Book, BookAuthor, BookCategory
from ..forms import BookEditForm
from ..mixins import DeleteMixin


@login_required
def create_book(request):
    form = BookEditForm(request.POST or None)
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
    books_info = []
    for book in books:
        book_author_rels = BookAuthor.objects.select_related(
            'author').filter(book=book)
        book_category_rels = BookCategory.objects.select_related(
            'category').filter(book=book)
        books_info.append({
            'book': book,
            'authors': [ba.author.name for ba in book_author_rels],
            'categories': [bc.category.name for bc in book_category_rels]
        })
    return render(request, 'dashboard/list_books.html', {'books_info': books_info})


@login_required
def update_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book_author_rels = BookAuthor.objects.select_related(
        'author').filter(book=book)
    book_category_rels = BookCategory.objects.select_related(
        'category').filter(book=book)
    form = BookEditForm(request.POST or None, initial={
        'title': book.title,
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
                form.update(book, book_author_rels, book_category_rels)
            return redirect('dashboard:list-books')
    return render(request, 'dashboard/generic_edit.html', context)


class BookDeleteView(DeleteMixin):
    model = Book
    success_url = reverse_lazy('dashboard:list-books')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Book', **kwargs)

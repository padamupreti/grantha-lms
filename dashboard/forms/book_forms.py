from django import forms
from django.core.exceptions import ValidationError

from ..models import Author, Publisher, Category, Book, BookAuthor, BookCategory, BookCopy


class BookCreateForm(forms.Form):
    title = forms.CharField()
    quantity = forms.IntegerField(min_value=1)
    # TODO add ISBN number validation
    isbn = forms.CharField(label='ISBN', required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(
    ), label='Authors (Hold Ctrl or Command to select multiple)')
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all())
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(
    ), label='Categories (Hold Ctrl or Command to select multiple)')

    def create(self):
        data = self.cleaned_data
        book = Book.objects.create(
            title=data['title'], isbn=data['isbn'], publisher=data['publisher'])
        for author in data['authors']:
            BookAuthor.objects.create(book=book, author=author)
        for category in data['categories']:
            BookCategory.objects.create(book=book, category=category)
        book_copies = [
            BookCopy(book=book, is_available=True)] * data['quantity']
        BookCopy.objects.bulk_create(book_copies)


class BookUpdateForm(BookCreateForm):
    quantity = forms.IntegerField(min_value=0)

    def __init__(self, *args, book=None, book_author_rels=None, book_category_rels=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book
        self.book_author_rels = book_author_rels
        self.book_category_rels = book_category_rels

    def clean_quantity(self):
        updated_quantity = self.cleaned_data['quantity']
        issued_count = BookCopy.objects.filter(
            book=self.book, is_available=False).count()
        if updated_quantity < issued_count:
            raise ValidationError(
                f'Quantity must be >= {issued_count} copies issued currently.')
        return updated_quantity

    def update(self):
        data = self.cleaned_data

        # Update Book-Author Relationships
        updated_authors = data['authors']
        for ba in self.book_author_rels:
            if ba.author not in updated_authors:
                ba.delete()
        for author in updated_authors:
            BookAuthor.objects.update_or_create(
                book=self.book, author=author)

        # Update Book-Category Relationships
        updated_categories = data['categories']
        for bc in self.book_category_rels:
            if bc.category not in updated_categories:
                bc.delete()
        for category in updated_categories:
            BookCategory.objects.update_or_create(
                book=self.book, category=category)

        # Update Book model data
        Book.objects.filter(id=self.book.id).update(title=data['title'], isbn=data['isbn'],
                                                    publisher=data['publisher'])

        # Update number of copies as appropriate
        current_copies = BookCopy.objects.filter(book=self.book)
        copies_count = current_copies.count()
        updated_quantity = self.cleaned_data['quantity']
        if not updated_quantity == copies_count:
            if updated_quantity > copies_count:
                additional_count = updated_quantity - copies_count
                additional_copies = [
                    BookCopy(book=self.book, is_available=True)] * additional_count
                BookCopy.objects.bulk_create(additional_copies)
            else:
                deletion_count = copies_count - updated_quantity
                available_copies = current_copies.filter(is_available=True)
                BookCopy.objects.filter(id__in=list(
                    available_copies.values_list('id', flat=True)[:deletion_count])
                ).delete()

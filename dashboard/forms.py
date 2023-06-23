from django import forms

from .models import Author, Publisher, Category, Book, BookAuthor, BookCategory  # , BookCopy


class BookEditForm(forms.Form):
    title = forms.CharField()
    # TODO add ISBN number validation
    isbn = forms.CharField(label='ISBN', required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(
    ), label='Authors (Hold Ctrl or Command to select multiple)')
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all())
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(
    ), label='Categories (Hold Ctrl or Command to select multiple)')
    # quantity = forms.IntegerField(min_value=1, max_value=len(
    #     BookCopy.objects.filter(is_available=True)))

    def create(self):
        data = self.cleaned_data
        book = Book.objects.create(
            title=data['title'], isbn=data['isbn'], publisher=data['publisher'])
        for author in data['authors']:
            BookAuthor.objects.create(book=book, author=author)
        for category in data['categories']:
            BookCategory.objects.create(book=book, category=category)
        # for _ in range(data['quantity']):
        #     BookCopy.objects.create(book=book, is_available=True)

    def update(self, book, book_author_rels, book_category_rels):
        data = self.cleaned_data
        # Update Book-Author Relationships
        updated_authors = data['authors']
        for ba in book_author_rels:
            if ba.author not in updated_authors:
                ba.delete()
        for author in updated_authors:
            BookAuthor.objects.update_or_create(
                book=book, author=author)
        # Update Book-Category Relationships
        updated_categories = data['categories']
        for bc in book_category_rels:
            if bc.category not in updated_categories:
                bc.delete()
        for category in updated_categories:
            BookCategory.objects.update_or_create(
                book=book, category=category)
        # Update Book data
        Book.objects.filter(id=book.id).update(title=data['title'], isbn=data['isbn'],
                                               publisher=data['publisher'])
        # Change number of copies as necessary
        # updated_quantity = data['quantity']
        # copies_quantity = len(BookCopy.objects.filter(book=book))
        # if not updated_quantity == copies_quantity:
        #     if updated_quantity > copies_quantity:
        #         diff = updated_quantity - copies_quantity
        #         for _ in range(diff):
        #             BookCopy.objects.create(book=book, is_available=True)
        #     else:
        #         diff = copies_quantity - updated_quantity
        #         bc_queryset = BookCopy.objects.filter(is_available=True)[diff:].delete()

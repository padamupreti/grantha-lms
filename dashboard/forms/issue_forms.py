from django import forms
from django.core.exceptions import ValidationError

from datetime import date, timedelta

from ..models import Book, Author, BookAuthor, BookCopy, Issue
from authentication.models import LMSUser


def get_unique_book_choices():
    qs = Book.objects.values_list('title', flat=True)
    unique_set = set(list(qs))
    choice_tuples = [('', '---------')] + [tuple([i] * 2)
                                           for i in list(unique_set)]
    return choice_tuples


class IssueCreateForm(forms.Form):
    book = forms.ChoiceField(choices=get_unique_book_choices())
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    member = forms.ModelChoiceField(
        queryset=LMSUser.objects.filter(is_superuser=False, is_librarian=False))
    issue_date = forms.DateField(initial=date.today(), disabled=True)
    due_date = forms.DateField(initial=date.today() + timedelta(days=5))

    def clean_member(self):
        member = self.cleaned_data['member']
        member_issues = Issue.objects.filter(
            member=member, returned_date=None)
        for issue in member_issues:
            if issue.due_date < date.today():
                raise ValidationError(
                    'Selected member has overdue books required to be returned.')
        return member

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if date.today() >= due_date:
            raise ValidationError('Due date must occur after today.')
        return due_date

    def clean(self):
        # Obtain cleaned data
        cleaned_data = super().clean()

        # Find book(s) from input book title
        title = cleaned_data['book']
        matching_books = Book.objects.filter(title__exact=title)
        if len(matching_books) == 0:
            raise ValidationError(
                'Selected book was not found.')

        # Make sure at least one book among matching books is written by input author
        author = cleaned_data['author']
        book_author_rel = None
        for book in matching_books:
            book_author_rel = BookAuthor.objects.filter(
                book=book, author=author).first()
            if book_author_rel:
                break
        if book_author_rel is None:
            raise ValidationError(
                f'No title {title} by {author} found in Library.')

        # Make sure book to issue has available copies
        book = book_author_rel.book
        copy = BookCopy.objects.filter(
            book=book, is_available=True).first()
        if copy is None:
            raise ValidationError(
                'Selected book has no available copies to issue.')

        # Update cleaned data with book copy (in place of title)
        cleaned_data.update({'book': copy})
        return cleaned_data

    def create(self):
        data = self.cleaned_data
        copy = data['book']
        copy.is_available = False
        copy.save()
        Issue.objects.create(book_copy=copy, member=data['member'],
                             issue_date=data['issue_date'], due_date=data['due_date'])

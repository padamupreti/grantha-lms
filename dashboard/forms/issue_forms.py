from django import forms
from django.core.exceptions import ValidationError

from datetime import date, timedelta

from ..models import Book, BookCopy, Issue
from authentication.models import LMSUser


class IssueCreateForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    member = forms.ModelChoiceField(
        queryset=LMSUser.objects.filter(is_superuser=False, is_librarian=False))
    due_date = forms.DateField(initial=date.today() + timedelta(days=1))

    def clean_book(self):
        book = self.cleaned_data['book']
        copy = BookCopy.objects.filter(
            book=book, is_available=True).first()
        if copy is None:
            raise ValidationError(
                'Selected book has no available copies to issue.')
        copy.is_available = False
        copy.save()
        return copy

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if date.today() >= due_date:
            raise ValidationError('Due date must occur after today.')
        return due_date

    def create(self):
        data = self.cleaned_data
        Issue.objects.create(book_copy=data['book'], member=data['member'],
                             issue_date=date.today(), due_date=data['due_date'])

from django import forms
from django.core.exceptions import ValidationError

from datetime import date, timedelta

from ..models import Book, BookCopy, Issue
from authentication.models import LMSUser


class IssueCreateForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    member = forms.ModelChoiceField(
        queryset=LMSUser.objects.filter(is_superuser=False, is_librarian=False))
    issue_date = forms.DateField(initial=date.today(), disabled=True)
    due_date = forms.DateField(initial=date.today() + timedelta(days=5))

    def clean_book(self):
        book = self.cleaned_data['book']
        copy = BookCopy.objects.filter(
            book=book, is_available=True).first()
        if copy is None:
            raise ValidationError(
                'Selected book has no available copies to issue.')
        return copy

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

    def create(self):
        data = self.cleaned_data
        copy = data['book']
        copy.is_available = False
        copy.save()
        Issue.objects.create(book_copy=copy, member=data['member'],
                             issue_date=data['issue_date'], due_date=data['due_date'])

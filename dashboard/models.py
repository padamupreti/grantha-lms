from django.db import models
from django.urls import reverse

from authentication.models import LMSUser


class Author(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:list-authors')


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:list-publishers')


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dashboard:list-categories')


class Book(models.Model):
    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    publisher = models.ForeignKey(
        Publisher, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title}'s Author - {self.author.name}"


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title}'s Category - {self.category.name}"


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_available = models.BooleanField()

    def __str__(self):
        return f"{self.book.title} - Copy ID #{self.id}"


class Request(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, null=True, on_delete=models.SET_NULL)
    request_date = models.DateField()
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f'Request#{self.id} on {self.request_date}'


class Issue(models.Model):
    book_copy = models.ForeignKey(
        BookCopy, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField()
    request = models.OneToOneField(
        Request, blank=True, null=True, on_delete=models.SET_NULL)
    due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return f'Issue#{self.id} on {self.issue_date}'


class LateFine(models.Model):
    book_copy = models.ForeignKey(
        BookCopy, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, on_delete=models.CASCADE)
    late_days = models.IntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    fined_date = models.DateField()

    def __str__(self):
        return f'LateFine#{self.id} for {self.member.username} on {self.fined_date}'

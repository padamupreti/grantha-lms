from django.db import models

from authentication.models import LMSUser


class Author(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.name


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
        return f"Copy #{self.id} of {self.book.title}"


class Issue(models.Model):
    book_copy = models.ForeignKey(
        BookCopy, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, null=True, on_delete=models.SET_NULL)
    issue_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f'{self.book_copy.book.title} #{self.book_copy.id} to {self.member.username} ({self.issue_date})'


class Request(models.Model):
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, null=True, on_delete=models.SET_NULL)
    request_date = models.DateField()
    is_fulfilled = models.BooleanField()

    def __str__(self):
        return f'{self.book.title} request by {self.member.username} ({self.request_date})'


class LateFine(models.Model):
    book_copy = models.ForeignKey(
        BookCopy, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(LMSUser, on_delete=models.CASCADE)
    late_days = models.IntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    fined_date = models.DateField()

    def __str__(self):
        return f'{self.member.username} for {self.book_copy.book.title} ({self.fined_date})'

from django.contrib import admin

from .models import (Author, Publisher, Category, Book,
                     BookAuthor, BookCategory, BookCopy, Issue,
                     Request, LateFine)

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)
admin.site.register(BookCopy)
admin.site.register(Issue)
admin.site.register(Request)
admin.site.register(LateFine)

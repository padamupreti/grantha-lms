from django.urls import path

from .views.general import home
from .views.author import AuthorCreateView, list_authors, AuthorUpdateView, AuthorDeleteView
from .views.publisher import PublisherCreateView, list_publishers, PublisherUpdateView, PublisherDeleteView
from .views.category import CategoryCreateView, list_categories, CategoryUpdateView, CategoryDeleteView
from .views.book import create_book, list_books, book_detail, update_book, BookDeleteView
from .views.issue import issue_book, list_issues, return_issued_book
from .views.fine import FineListView
from .views.book_request import request_book, BookRequestList

app_name = 'dashboard'
urlpatterns = [
    # Dashboard home
    path('home/', home, name='home'),
    # Authors
    path('authors/', list_authors, name='list-authors'),
    path('authors/new/', AuthorCreateView.as_view(), name='create-author'),
    path('authors/<int:pk>/update/',
         AuthorUpdateView.as_view(), name='update-author'),
    path('authors/<int:pk>/delete/',
         AuthorDeleteView.as_view(), name='delete-author'),
    # Publishers
    path('publishers/', list_publishers, name='list-publishers'),
    path('publishers/new/', PublisherCreateView.as_view(), name='create-publisher'),
    path('publishers/<int:pk>/update/',
         PublisherUpdateView.as_view(), name='update-publisher'),
    path('publishers/<int:pk>/delete/',
         PublisherDeleteView.as_view(), name='delete-publisher'),
    # Categories
    path('categories/', list_categories, name='list-categories'),
    path('categories/new/', CategoryCreateView.as_view(), name='create-category'),
    path('categories/<int:pk>/update/',
         CategoryUpdateView.as_view(), name='update-category'),
    path('categories/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name='delete-category'),
    # Books
    path('books/', list_books, name='list-books'),
    path('books/new/', create_book, name='create-book'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/<int:pk>/update/', update_book, name='update-book'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete-book'),
    # Issue
    path('issues/', list_issues, name='list-issues'),
    path('issues/new/', issue_book, name='create-issue'),
    path('issues/<int:pk>/return/', return_issued_book, name='return-issued'),
    # Fines
    path('fines/', FineListView.as_view(), name='list-fines'),
    # Book Requests
    path('books/requests/', BookRequestList.as_view(), name='book-requests'),
    path('books/requests/<int:pk>/', request_book, name='request-book')
]

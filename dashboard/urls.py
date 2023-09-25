from django.urls import path

from .views.general import home, browse_books
from .views.author import AuthorCreateView, list_authors, AuthorUpdateView, delete_author
from .views.publisher import PublisherCreateView, list_publishers, PublisherUpdateView, delete_publisher
from .views.category import CategoryCreateView, list_categories, CategoryUpdateView, delete_category
from .views.book import create_book, list_books, book_detail, update_book, delete_book
from .views.issue import issue_book, list_issues, return_issued_book
from .views.fine import list_fines
from .views.book_request import request_book, list_book_requests
from .views.member import members_list, member_info, member_report

app_name = 'dashboard'
urlpatterns = [
    # Dashboard home
    path('home/', home, name='home'),
    path('browse/', browse_books, name='browse'),
    # Authors
    path('authors/', list_authors, name='list-authors'),
    path('authors/new/', AuthorCreateView.as_view(), name='create-author'),
    path('authors/<int:pk>/update/',
         AuthorUpdateView.as_view(), name='update-author'),
    path('authors/<int:pk>/delete/',
         delete_author, name='delete-author'),
    # Publishers
    path('publishers/', list_publishers, name='list-publishers'),
    path('publishers/new/', PublisherCreateView.as_view(), name='create-publisher'),
    path('publishers/<int:pk>/update/',
         PublisherUpdateView.as_view(), name='update-publisher'),
    path('publishers/<int:pk>/delete/',
         delete_publisher, name='delete-publisher'),
    # Categories
    path('categories/', list_categories, name='list-categories'),
    path('categories/new/', CategoryCreateView.as_view(), name='create-category'),
    path('categories/<int:pk>/update/',
         CategoryUpdateView.as_view(), name='update-category'),
    path('categories/<int:pk>/delete/',
         delete_category, name='delete-category'),
    # Books
    path('books/', list_books, name='list-books'),
    path('books/new/', create_book, name='create-book'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/<int:pk>/update/', update_book, name='update-book'),
    path('books/<int:pk>/delete/', delete_book, name='delete-book'),
    # Issue
    path('issues/', list_issues, name='list-issues'),
    path('issues/new/', issue_book, name='create-issue'),
    path('issues/<int:pk>/return/', return_issued_book, name='return-issued'),
    # Fines
    path('fines/', list_fines, name='list-fines'),
    # Book Requests
    path('books/requests/', list_book_requests, name='book-requests'),
    path('books/requests/<int:pk>/', request_book, name='request-book'),
    # Members
    path('members/', members_list, name='list-members'),
    path('members/<int:pk>/', member_info, name='member-detail'),
    path('members/<int:pk>/report/', member_report, name='member-report')
]

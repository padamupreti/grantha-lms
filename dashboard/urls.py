from django.urls import path

from .views.general import home
from .views.author import AuthorCreateView, AuthorListView, AuthorUpdateView, AuthorDeleteView
from .views.publisher import PublisherCreateView, PublisherListView, PublisherUpdateView, PublisherDeleteView
from .views.category import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView

app_name = 'dashboard'
urlpatterns = [
    # Dashboard home
    path('', home, name='home'),
    # Authors
    path('authors/new/', AuthorCreateView.as_view(), name='create-author'),
    path('authors/', AuthorListView.as_view(), name='list-authors'),
    path('authors/<int:pk>/update/',
         AuthorUpdateView.as_view(), name='update-author'),
    path('authors/<int:pk>/delete/',
         AuthorDeleteView.as_view(), name='delete-author'),
    # Publishers
    path('publishers/', PublisherListView.as_view(), name='list-publishers'),
    path('publishers/new/', PublisherCreateView.as_view(), name='create-publisher'),
    path('publishers/<int:pk>/update/',
         PublisherUpdateView.as_view(), name='update-publisher'),
    path('publishers/<int:pk>/delete/',
         PublisherDeleteView.as_view(), name='delete-publisher'),
    # Categories
    path('categories/', CategoryListView.as_view(), name='list-categories'),
    path('categories/new/', CategoryCreateView.as_view(), name='create-category'),
    path('categories/<int:pk>/update/',
         CategoryUpdateView.as_view(), name='update-category'),
    path('categories/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name='delete-category'),
]

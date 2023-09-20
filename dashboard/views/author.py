from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Author


class AuthorCreateView(EditMixin, LibrarianView, CreateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


def list_authors(request):
    return list_card_items(request, Author, 'dashboard/author_cards.html', 'dashboard/list_authors.html')


class AuthorUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorDeleteView(DeleteMixin, LibrarianView):
    model = Author
    success_url = reverse_lazy('dashboard:list-authors')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)

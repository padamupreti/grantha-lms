from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Author


class AuthorCreateView(EditMixin, LibrarianView, CreateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorListView(ListView):
    model = Author
    template_name = 'dashboard/list_authors.html'


class AuthorUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorDeleteView(DeleteMixin, LibrarianView):
    model = Author
    success_url = reverse_lazy('dashboard:list-authors')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)

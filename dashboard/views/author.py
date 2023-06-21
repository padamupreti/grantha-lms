from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from ..mixins import EditMixin, DeleteMixin
from ..models import Author


class AuthorCreateView(EditMixin, CreateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'dashboard/list_authors.html'


class AuthorUpdateView(EditMixin, UpdateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorDeleteView(DeleteMixin):
    model = Author
    success_url = reverse_lazy('dashboard:list-authors')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)

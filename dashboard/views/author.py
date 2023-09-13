from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Author


class AuthorCreateView(EditMixin, LibrarianView, CreateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


def list_authors(request):
    query_params = request.GET
    p_author_name = query_params.get('query')

    qs = Author.objects.all()
    if p_author_name:
        qs = qs.filter(name__icontains=p_author_name)

    template_name = 'dashboard/author_cards.html'
    if not request.user.is_anonymous and request.user.is_librarian:
        template_name = 'dashboard/list_authors.html'

    context = {
        'object_list': qs,
        'search_placeholder': 'Search by author name',
        'query_text': p_author_name
    }

    return render(request, template_name, context)


class AuthorUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Author

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)


class AuthorDeleteView(DeleteMixin, LibrarianView):
    model = Author
    success_url = reverse_lazy('dashboard:list-authors')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Author', **kwargs)

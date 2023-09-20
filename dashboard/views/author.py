from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError

from authentication.decorators import only_librarians

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin
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


@login_required
@only_librarians
def delete_author(request, pk):
    author = get_object_or_404(Author, id=pk)

    if request.method == 'POST':
        try:
            author.delete()
            return redirect(reverse_lazy('dashboard:list-authors'))
        except ProtectedError:
            messages.error(
                request, f'Author {author} is referenced in book record.')
            return redirect('dashboard:list-authors')

    context = {
        'item_type': 'Author',
        'object': author
    }

    return render(request, 'dashboard/generic_delete.html', context)

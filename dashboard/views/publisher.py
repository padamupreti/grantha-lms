from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError

from authentication.decorators import only_librarians

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin
from ..models import Publisher


class PublisherCreateView(EditMixin, LibrarianView, CreateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


def list_publishers(request):
    return list_card_items(request, Publisher, 'dashboard/publisher_cards.html', 'dashboard/list_publishers.html')


class PublisherUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


@login_required
@only_librarians
def delete_publisher(request, pk):
    publisher = get_object_or_404(Publisher, id=pk)

    if request.method == 'POST':
        try:
            publisher.delete()
            return redirect(reverse_lazy('dashboard:list-publishers'))
        except ProtectedError:
            messages.error(
                request, f'Publisher {publisher} is referenced in book record.')
            return redirect('dashboard:list-publishers')

    context = {
        'item_type': 'Publisher',
        'object': publisher
    }

    return render(request, 'dashboard/generic_delete.html', context)

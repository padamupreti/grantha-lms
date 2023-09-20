from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin, DeleteMixin
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


class PublisherDeleteView(DeleteMixin, LibrarianView):
    model = Publisher
    success_url = reverse_lazy('dashboard:list-publishers')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)

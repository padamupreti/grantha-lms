from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Publisher


class PublisherCreateView(EditMixin, LibrarianView, CreateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


class PublisherListView(ListView):
    model = Publisher
    template_name = 'dashboard/list_publishers.html'


class PublisherUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


class PublisherDeleteView(DeleteMixin, LibrarianView):
    model = Publisher
    success_url = reverse_lazy('dashboard:list-publishers')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)

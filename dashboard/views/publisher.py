from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Publisher


class PublisherCreateView(EditMixin, LibrarianView, CreateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


def list_publishers(request):
    query_params = request.GET
    p_publisher_name = query_params.get('query')

    qs = Publisher.objects.all()
    if p_publisher_name:
        qs = qs.filter(name__icontains=p_publisher_name)

    template_name = 'dashboard/publisher_cards.html'
    if not request.user.is_anonymous and request.user.is_librarian:
        template_name = 'dashboard/list_publishers.html'

    context = {
        'object_list': qs,
        'search_placeholder': 'Search by publisher name',
        'query_text': p_publisher_name
    }

    return render(request, template_name, context)


class PublisherUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Publisher

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)


class PublisherDeleteView(DeleteMixin, LibrarianView):
    model = Publisher
    success_url = reverse_lazy('dashboard:list-publishers')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Publisher', **kwargs)

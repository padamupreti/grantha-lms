from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Category


class CategoryCreateView(EditMixin, LibrarianView, CreateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


def list_categories(request):
    query_params = request.GET
    p_category_name = query_params.get('query')

    qs = Category.objects.all()
    if p_category_name:
        qs = qs.filter(name__icontains=p_category_name)

    template_name = 'dashboard/category_cards.html'
    if not request.user.is_anonymous and request.user.is_librarian:
        template_name = 'dashboard/list_categories.html'

    context = {
        'object_list': qs,
        'search_placeholder': 'Search by category name',
    }

    return render(request, template_name, context)


class CategoryUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


class CategoryDeleteView(DeleteMixin, LibrarianView):
    model = Category
    success_url = reverse_lazy('dashboard:list-categories')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)

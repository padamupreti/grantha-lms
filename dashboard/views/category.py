from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Category


class CategoryCreateView(EditMixin, LibrarianView, CreateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


def list_categories(request):
    return list_card_items(request, Category, 'dashboard/category_cards.html', 'dashboard/list_categories.html')


class CategoryUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


class CategoryDeleteView(DeleteMixin, LibrarianView):
    model = Category
    success_url = reverse_lazy('dashboard:list-categories')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)

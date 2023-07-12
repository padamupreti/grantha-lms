from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .general import LibrarianView
from ..mixins import EditMixin, DeleteMixin
from ..models import Category


class CategoryCreateView(EditMixin, LibrarianView, CreateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/list_categories.html'


class CategoryUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


class CategoryDeleteView(DeleteMixin, LibrarianView):
    model = Category
    success_url = reverse_lazy('dashboard:list-categories')

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)

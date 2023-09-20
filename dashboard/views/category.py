from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError

from authentication.decorators import only_librarians

from .general import list_card_items, LibrarianView
from ..mixins import EditMixin
from ..models import Category


class CategoryCreateView(EditMixin, LibrarianView, CreateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


def list_categories(request):
    return list_card_items(request, Category, 'dashboard/category_cards.html', 'dashboard/list_categories.html', 'category')


class CategoryUpdateView(EditMixin, LibrarianView, UpdateView):
    model = Category

    def get_context_data(self, **kwargs):
        return super().get_context_data('Category', **kwargs)


@login_required
@only_librarians
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == 'POST':
        try:
            category.delete()
            return redirect(reverse_lazy('dashboard:list-categories'))
        except ProtectedError:
            messages.error(
                request, f'Category {category} is referenced in book record.')
            return redirect('dashboard:list-categories')

    context = {
        'item_type': 'Category',
        'object': category
    }

    return render(request, 'dashboard/generic_delete.html', context)

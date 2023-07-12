# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .general import LibrarianView

from ..models import LateFine


class FineListView(LoginRequiredMixin, LibrarianView, ListView):
    model = LateFine
    template_name = 'dashboard/list_fines.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView


class EditMixin(LoginRequiredMixin):
    template_name = 'dashboard/generic_edit.html'
    fields = '__all__'

    def get_context_data(self, item_type, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = item_type
        return context


class DeleteMixin(EditMixin, DeleteView):
    template_name = 'dashboard/generic_delete.html'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from authentication.decorators import only_librarians

from ..models import LateFine


@login_required
@only_librarians
def list_fines(request):
    query_params = request.GET
    p_title = query_params.get('query')

    fines = LateFine.objects.order_by('-fined_date')
    if p_title:
        fines = fines.filter(book_copy__book__title__icontains=p_title)

    context = {
        'object_list': fines,
        'search_placeholder': 'Search by book title',
        'query_text': p_title
    }

    return render(request, 'dashboard/list_fines.html', context)

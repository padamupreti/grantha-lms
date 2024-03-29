from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View

from datetime import date, timedelta
from secrets import choice

from authentication.decorators import exclude_librarians

from ..models import Book, BookCopy, Issue, Request, LateFine, Category, BookCategory
from ..utils import add_is_due, add_book_attributes


def member_home(request, shared_context):
    context = shared_context

    issues = Issue.objects.filter(
        member=request.user, returned_date=None).order_by('due_date')
    add_is_due(issues)
    requests = Request.objects.filter(
        member=request.user, is_fulfilled=False)
    late_fines = LateFine.objects.filter(
        member=request.user).order_by('-fined_date')

    context.update({
        'issues': issues,
        'requests': requests,
        'late_fines': late_fines
    })

    return render(request, 'dashboard/member_home.html', context)


def librarian_home(request, shared_context):
    context = shared_context

    issues = Issue.objects.filter(
        returned_date=None).order_by('due_date')
    add_is_due(issues)
    overdue_count = issues.filter(
        due_date__lte=date.today()).count()
    requests = Request.objects.filter(
        is_fulfilled=False).order_by('request_date')

    context.update({
        'issues': issues[:5],
        'issues_count': issues.count(),
        'overdue_count': overdue_count,
        'requests': requests[:5],
        'requests_count': requests.count()
    })

    return render(request, 'dashboard/librarian_home.html', context)


@exclude_librarians
def browse_books(request):
    seven_d_before = date.today() - timedelta(days=7)
    latest_issues = Issue.objects.filter(issue_date__gte=seven_d_before)
    books = [i.book_copy.book for i in latest_issues if i.book_copy]
    unique_books = list(set(books))
    for b in unique_books:
        add_book_attributes(b, request)
        b.issues_count = latest_issues.filter(book_copy__book__id=b.id).count()
    unique_books.sort(key=lambda b: b.issues_count, reverse=True)

    categories = Category.objects.all()
    random_category = None
    category_books = []
    if categories:
        random_category = choice(categories)
        categories = categories.exclude(id=random_category.id)

        book_category_rels = BookCategory.objects.filter(
            category=random_category)
        category_books = [bc.book for bc in book_category_rels]
        for b in category_books:
            add_book_attributes(b, request)

    context = {
        'popular_books': unique_books[:5],
        'random_category': random_category,
        'category_books': category_books[:5],
        'categories': categories[:5]
    }

    return render(request, 'dashboard/browse.html', context)


def home(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:browse')

    books = Book.objects.all()
    total_books_count = books.count()

    available_books_count = 0
    for book in books:
        available_copies = BookCopy.objects.filter(
            book=book, is_available=True).count()
        if available_copies > 0:
            available_books_count += 1

    context = {
        'total_books_count': total_books_count,
        'available_books_count': available_books_count
    }

    if request.user.is_librarian:
        return librarian_home(request, context)
    return member_home(request, context)


def list_card_items(request, model, cards_template, list_template, model_name):
    query_params = request.GET
    p_name = query_params.get('query')

    qs = model.objects.all()
    if p_name:
        qs = qs.filter(name__icontains=p_name)

    template_name = cards_template
    if request.user.is_authenticated and request.user.is_librarian:
        template_name = list_template

    context = {
        'object_list': qs,
        'search_placeholder': f'Search by {model_name} name',
        'query_text': p_name
    }

    return render(request, template_name, context)


class LibrarianView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_librarian

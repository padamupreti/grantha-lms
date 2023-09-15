from xhtml2pdf import pisa

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template

from datetime import date, datetime

from authentication.decorators import only_librarians
from authentication.models import LMSUser

from qrmanager import get_encoded_member_qr

from ..models import Issue, Request, LateFine


@login_required
@only_librarians
def members_list(request):
    query_params = request.GET
    p_member_name = query_params.get('query')

    qs = LMSUser.objects.filter(is_superuser=False, is_librarian=False)
    if p_member_name:
        qs = qs.filter(username__icontains=p_member_name)

    context = {
        'object_list': qs,
        'search_placeholder': 'Search by username',
        'query_text': p_member_name
    }

    return render(request, 'dashboard/list_members.html', context)


@login_required
@only_librarians
def member_info(request, pk):
    qs = LMSUser.objects.filter(is_superuser=False, is_librarian=False)
    member = get_object_or_404(qs, id=pk)
    encoded_qr = get_encoded_member_qr(request.get_host(), member)

    issues = Issue.objects.filter(
        member=member).order_by('returned_date')
    for issue in issues:
        issue.is_due = False
        if issue.due_date <= date.today() and issue.returned_date is None:
            issue.is_due = True

    requests = Request.objects.filter(member=member).order_by('is_fulfilled')
    late_fines = LateFine.objects.filter(member=member).order_by('-fined_date')

    context = {
        'encoded_qr': encoded_qr,
        'member': member,
        'issues': issues,
        'requests': requests,
        'late_fines': late_fines
    }

    return render(request, 'dashboard/member_detail.html', context)


@login_required
@only_librarians
def member_report(request, pk):
    qs = LMSUser.objects.filter(is_superuser=False, is_librarian=False)
    member = get_object_or_404(qs, id=pk)
    encoded_qr = get_encoded_member_qr(request.get_host(), member)

    issues = Issue.objects.filter(
        member=member).order_by('returned_date')
    for issue in issues:
        issue.is_due = False
        if issue.due_date <= date.today() and issue.returned_date is None:
            issue.is_due = True

    requests = Request.objects.filter(member=member).order_by('is_fulfilled')
    late_fines = LateFine.objects.filter(member=member).order_by('-fined_date')
    datetime_now = datetime.now()

    context = {
        'now': datetime_now,
        'encoded_qr': encoded_qr,
        'member': member,
        'issues': issues,
        'requests': requests,
        'late_fines': late_fines
    }

    response = HttpResponse(content_type='application/pdf')
    file_title = f'LMS_Report_{member.username}#{member.id}_{datetime_now.isoformat()}'
    response['Content-Disposition'] = f'inline; filename="{file_title}.pdf"'

    template = get_template('dashboard/member_report.html')
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF report <pre>' + html + '</pre>')
    return response

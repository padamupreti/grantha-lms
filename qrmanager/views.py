from .forms import UploadFileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from authentication.decorators import only_members, only_librarians

from .utils import file_res_member_qr


@login_required
@only_members
def download_qr(request):
    return file_res_member_qr(request.get_host(), request.user)


@login_required
@only_librarians
def upload_qr(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect(form.redirect_path)
    else:
        form = UploadFileForm()
    return render(request, 'qrmanager/upload_qr.html', {'form': form})

from django import forms
from django.core.exceptions import ValidationError

from .utils import get_redirect_path


class UploadFileForm(forms.Form):
    qr_image = forms.ImageField(label='Member QR Image')

    def clean_qr_image(self):
        qr_image = self.cleaned_data['qr_image']
        success, redirect_path = get_redirect_path(qr_image)
        if not success:
            raise ValidationError(
                'Uploaded image is invalid QR or not detected properly.')
        self.redirect_path = redirect_path
        return qr_image

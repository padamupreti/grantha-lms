from io import BytesIO
from base64 import b64encode
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from django.urls import reverse
from django.http import FileResponse
from django.conf import settings

from qrcode import QRCode
import cv2


def load_buffer_qr(data, buffer):
    qr = QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(buffer, format='PNG')
    buffer.seek(0)


def file_res_member_qr(hostname, member):
    data = 'http://' + hostname + \
        reverse('dashboard:member-detail', args=[member.id])
    buffer = BytesIO()
    load_buffer_qr(data, buffer)
    filename = f'GLMS_Member_{member.id}_QR.png'
    return FileResponse(buffer, as_attachment=True, filename=filename)


def get_encoded_member_qr(hostname, member):
    data = 'http://' + hostname + \
        reverse('dashboard:member-detail', args=[member.id])
    buffer = BytesIO()
    load_buffer_qr(data, buffer)
    encoded_qr = b64encode(buffer.getvalue()).decode()
    return encoded_qr


def get_redirect_path(upload_image):
    # Read image with opencsv or fail
    image = None
    with NamedTemporaryFile() as f:
        for chunk in upload_image.chunks():
            f.write(chunk)
        f.seek(0)

        image = cv2.imread(f.name)
    if image is None:
        return False, 0

    # Get QR data or fail
    detector = cv2.QRCodeDetector()
    member_url, points, _ = detector.detectAndDecode(image)
    if points is None:
        return False, 0

    # Validate + Parse URL and get member id or fail
    try:
        o = urlparse(member_url)
        if not o.hostname in settings.ALLOWED_HOSTS:
            return False, 0

        # Return redirect path successfully
        return True, o.path
    except:
        return False, 0

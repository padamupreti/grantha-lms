from django.contrib.auth.forms import UserCreationForm

from .models import LMSUser


class LMSUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = LMSUser

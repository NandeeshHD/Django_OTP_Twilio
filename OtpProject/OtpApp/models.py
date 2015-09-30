from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(_('phone number'), max_length=15,
        help_text=_('Field to save the phone number of the user.'))
    
    is_verified = models.BooleanField(_('verified'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'verified.'))
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username_not_me(username):
    if username == 'me':
        raise ValidationError(
            _("%(username)s is not suitable"),
            params={"username": username},
        )

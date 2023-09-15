from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_pattern_symbols(username):
    pattern = re.compile("^[\w.@+-]+\Z")
    if not pattern.match(username):
        raise ValidationError(
            _('%(username)s is not allowed'),
            params={'username': username},
        )

def max_length(str):
    if len(str) > 150:
        raise ValidationError('length longer ')

def max_length254(str):
    if len(str) > 254:
        raise ValidationError('length longer ')

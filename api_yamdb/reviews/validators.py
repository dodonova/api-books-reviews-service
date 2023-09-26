from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api_yamdb.settings import MAX_SCORE, MIN_SCORE


def validate_year_number(year):
    if year > datetime.now().year or year < 1:
        raise ValidationError(
            _("%(year)s is not allowed"),
            params={"year": year},
        )


def validate_score(score):
    if score > MAX_SCORE or score < MIN_SCORE:
        raise ValidationError(
            _(f"%(score)s must be from {MIN_SCORE} to {MAX_SCORE} points"),
            params={"score": score},
        )

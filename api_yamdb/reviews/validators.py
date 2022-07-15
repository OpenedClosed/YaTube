import datetime

from django.forms import ValidationError


def year_validate(value):
    if value <= datetime.date.today().year:
        return value
    raise ValidationError('Введите год не больше текущего')

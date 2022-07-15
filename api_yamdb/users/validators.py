from django.core.exceptions import ValidationError


def username_validate(value):
    if value == 'me':
        raise ValidationError('Пожалуйста, придумайте другое имя')
    return value


def role_validate(value):
    if value == 'user' or value == 'moderator' or value == 'admin':
        return value
    raise ValidationError(
        'Пожалуйста, введите "user" или "moderator" или "admin"'
    )

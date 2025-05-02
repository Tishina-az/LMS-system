import re

from rest_framework.exceptions import ValidationError


class LinkValidator:
    """Валидирует ссылки на сторонние ресурсы, кроме youtube.com."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = re.compile(r'^(https?:\/\/)?(www\.)?(youtube\.com)\/.+')
        tmp_link = dict(value).get(self.field)
        if not bool(link.match(tmp_link)):
            raise ValidationError('Введите корректную ссылку на YouTube (youtube.com).')

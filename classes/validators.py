from rest_framework.serializers import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = 'youtube.com'
        valid = dict(value).get(self.field)
        if valid:
            if link not in valid:
                raise ValidationError('Материал можно использовать только с youtube.com')

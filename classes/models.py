from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to="previews/", verbose_name="превью", **NULLABLE)
    description = models.TextField(verbose_name='описание')

    lessons = models.ManyToManyField('Lesson', verbose_name='урок')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to="previews/", verbose_name="превью", **NULLABLE)
    video_link = models.URLField(verbose_name="ссылка на видео", **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Payment(models.Model):
    PAYMENT_METHOD = [
        ("cash", "наличные"),
        ("bank_transfer", "перевод"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments",
                                    verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments",
                                    verbose_name='оплаченный урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        return f"{self.user}: {self.payment_date} - {self.amount} - {self.payment_method}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    subscribed = models.BooleanField(default=True, verbose_name='Подписка')

    def __str__(self):
        return f'{self.course} {self.user} ({self.subscribed})'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

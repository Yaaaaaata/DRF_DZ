from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to="previews/", verbose_name="превью", **NULLABLE)
    description = models.TextField(verbose_name='описание')

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

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

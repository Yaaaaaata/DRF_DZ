# Generated by Django 4.2.6 on 2023-11-03 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_course_lessons_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lessons',
            field=models.ManyToManyField(to='classes.lesson', verbose_name='урок'),
        ),
    ]

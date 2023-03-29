# Generated by Django 4.1.7 on 2023-03-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_idea'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='actions',
            field=models.TextField(default=0, verbose_name='Действия'),
        ),
        migrations.AddField(
            model_name='idea',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
    ]

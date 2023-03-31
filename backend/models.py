from django.db import models
from django.conf import settings
import datetime

""" Дата создания/изменения/удаления"""


class DataTimeModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания',auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='Дата изменения',auto_now=True, editable=False)
    deleted = models.BooleanField(verbose_name='Запись удалена', default=False)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        ordering = ('-created_at',)
        abstract = True


class MainImage(DataTimeModel):
    date = models.ImageField(upload_to='{% static "use_image" %}', default="")


""" действия выводся списком, это временно, надо будет исправить"""

class Idea(DataTimeModel):
    is_active = models.BooleanField(verbose_name='Активный', default=False)
    author = models.CharField(verbose_name='Никнейм', max_length=22)
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    describe = models.TextField(verbose_name='Содержание')
    final_date = models.CharField(verbose_name='Дата окончания', max_length=255, default="")
    progress = models.IntegerField(verbose_name='Прогресс', default=0)
    actions = models.TextField(verbose_name='Действия', default="")

    def __str__(self) -> str:
        return f'{self.name}'


class Card(DataTimeModel):
    author = models.CharField(verbose_name='Никнейм', max_length=22)
    name = models.CharField(verbose_name='Заголовок', max_length=255)

    def __str__(self) -> str:
        return f'{self.author} {self.name}'
    

class Action(DataTimeModel):
    author = models.CharField(verbose_name='Никнейм', max_length=22)
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    card = models.ForeignKey(Card, verbose_name='карта', on_delete=models.CASCADE)
    describe = models.TextField(verbose_name='Содержание')
    date = models.CharField(verbose_name='Дата окончания', max_length=255)
    progress = models.IntegerField(verbose_name='Прогресс', default=0)
    complexity = models.IntegerField(verbose_name='сложность', default=0)
    importance = models.IntegerField(verbose_name='важность', default=0)

    def __str__(self) -> str:
        return f'{self.author} {self.card.name}'


class Comment(DataTimeModel):
    author = models.CharField(verbose_name='Никнейм', max_length=22)
    comment = models.TextField(verbose_name='Заголовок')
    action = models.ForeignKey(Action, verbose_name='Действие', on_delete=models.CASCADE, default="")

    def __str__(self) -> str:
        return f'{self.author} {self.comment}'
    

class Day(DataTimeModel):
    date = models.DateField(verbose_name='Дата')
    number = models.IntegerField(verbose_name='Номер', default=1)
    first_is_active = models.BooleanField(verbose_name='Воздержание', default=False)
    second_is_active = models.BooleanField(verbose_name='Порядок', default=False)
    third_is_active = models.BooleanField(verbose_name='Бережливость', default=False)
    fourth_is_active = models.BooleanField(verbose_name='Трудолюбие', default=False)

    def __str__(self) -> str:
        return f'{self.number}'

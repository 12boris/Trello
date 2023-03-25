from django.contrib.auth.models import AbstractUser
from django.db import models


# " все картинки загружаются в папку users_avatars. она создаётся авытоматически, но можно её переместить в другую папку, " \
# " например, в static/img, но тогда надо переписать путь:" \
# " upload_to='static/img/users_avatars' "

""" !!!! важно !!!! в файле settings нельзя удалять поле: AUTH_USER_MODEL = 'authapp.BaseIdeinerUser' """

class BaseIdeinerUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name="возраст", default=18)
    nickname = models.CharField(verbose_name="ник", max_length=40, default="")
    email = models.CharField(verbose_name="email", max_length=40, default="")
    username = models.CharField(verbose_name="username", max_length=40, unique=True, default="")
    surname = models.CharField(verbose_name="surname", max_length=40, default="")
    avatar = models.ImageField(upload_to="media/users_avatars", blank=True, default="")
    password = models.CharField(verbose_name="password", max_length=40, default="")
    registrationdate = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.password})"

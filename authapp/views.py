from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from backend.views import main

from authapp.forms import BaseIdeinerUserEditForm, BaseIdeinerUserLoginForm, BaseIdeinerUserRegisterForm


def login(request):
    title = "вход"

    login_form = BaseIdeinerUserLoginForm(data=request.POST or None)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)

            """ тут програма при авторизации перемещает в кабинет. это тестовая ссылка, её можно изменить на другую,
            например, главную страницу """

            return main(request)

    content = {"title": title, "login_form": login_form}
    return render(request, "authapp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("backend:index"))


def register(request):
    title = "регистрация"

    if request.method == "POST":
        register_form = BaseIdeinerUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("authapp:login"))
    else:
        register_form = BaseIdeinerUserRegisterForm()

    content = {"title": title, "register_form": register_form}
    return render(request, "authapp/register.html", content)


def cabinet(request):
    title = "Кабинет"

    name = request.user.username

    content = {"title": title, "name": name}
    return render(request, "authapp/cabinet.html", content)



def edit(request):
    title = "редактирование"

    if request.method == "POST":
        edit_form = BaseIdeinerUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("auth:edit"))
    else:
        edit_form = BaseIdeinerUserEditForm(instance=request.user)

    content = {"title": title, "edit_form": edit_form, "media_url": settings.MEDIA_URL}
    return render(request, "authapp/edit.html", content)

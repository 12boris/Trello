from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import HttpResponseRedirect, render
from .models import Card, Action, Comment, Week, Day
from authapp.models import BaseIdeinerUser
from django.contrib.auth.decorators import user_passes_test
import datetime


def GenIdeasList(cards):
    
    # генератор списка идей.
    # создаёт словарь, в котором ключ это порядковое число, а значение это словарь с отзывами и идеями
    # возвращает словарь со со всеми отзывами и идями
    # в html прогоняется циклом for item in ideas.values
    # в нём идеи вызываются так: item.idea, а отызывы так: item.feedback

    sl_ideas = {}
    a = 0
    for card in cards:
        a += 1
        sl_ideas[a] = {"action": Action.objects.filter(card=card).order_by("created_at"), "card": card}

    return sl_ideas


""" главное меню """


def main(request):
    title = "Карточки"

    card = GenIdeasList(Card.objects.all().order_by("created_at"))
    date = datetime.date.today().strftime('%d.%m.%y')

    content = {"title": title, "card": card, "date": date, "media_url": settings.MEDIA_URL}

    return render(request, "backend/index.html", content)


def calendar(request):
    title = "Календарь"
    weeks = Week.objects.all()
    days = Day.objects.all().order_by("week")

    content = {"title": title, "weeks": weeks, "media_url": settings.MEDIA_URL}

    return render(request, "backend/calendar.html", content)


""" дни """


def day_add(request):
    days = Day.objects.all()
    weeks = Week.objects.all()

    if days:
        last_day_date = days.last().date
        date = (last_day_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    else:
        date = (datetime.date.today()).strftime('%Y-%m-%d')
    
    try:
        last_week_number = weeks.last().number

    except:
        Week.objects.create(number=1).save()
        last_week_number = 1

    if len(days) % 7 == 0:
        new_week = Week.objects.create(number=last_week_number + 1)
        day = Day.objects.create(week=new_week, date=date)
        day.save()

    else:
        day = Day.objects.create(week=weeks.last(), date=date)
        day.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" карточки """


def card_add(request):

    name = request.POST['name']
    author = request.user.username

    new_card = Card.objects.create(name=name, author=author)
    new_card.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def card_delete(request, pk):

    card = Card.objects.filter(pk=pk)
    card.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" действия """


def action_card(request, pk):

    title = "Действие"
    action = Action.objects.filter(pk=pk).first()
    comments = Comment.objects.filter(action=action)
    date = datetime.date.today().strftime('%d.%m.%Y')

    content = {"title": title, "action": action, "date": date, "comments": comments, "media_url": settings.MEDIA_URL}

    return render(request, "backend/action_card.html", content)


def action_add(request):

    name_card = request.POST['name-card']
    card = Card.objects.filter(name=name_card).first()
    
    name = request.POST['name']
    date = request.POST['date']
    if str(date).lower() == "завтра":
        date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%y')

    if str(date).lower() == "сегодня":
        date = datetime.date.today().strftime('%d.%m.%y')

    describe = request.POST['describe']
    author = request.user.username

    new_action = Action.objects.create(name=name, author=author, date=date, describe=describe, card=card)
    new_action.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def action_edit(request, pk):
    
    action = Action.objects.filter(pk=pk).first()
    
    try:
        if request.POST["progress"]: action.progress = request.POST["progress"]
    except:pass

    try:    
        if request.POST["name"]: action.name = request.POST["name"]
        if request.POST["date"]: action.date = request.POST["date"]
        if request.POST["describe"]: action.describe = request.POST["describe"]
    except:
        pass

    action.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def action_delete(request, pk):
    
    action = Action.objects.filter(pk=pk)
    action.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" коментарии """


def comment_add(request, pk):
    
    action = Action.objects.filter(pk=pk).first()
    
    comment = request.POST['comment']
    author = request.user.username

    new_comment = Comment.objects.create(comment=comment, author=author, action=action)
    new_comment.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def comment_delete(request, pk):
    
    comment = Comment.objects.filter(pk=pk)
    comment.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" админка """

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    title = "Админка"
    
    card = Card.objects.all()

    content = {"title": title, "card": card, "media_url": settings.MEDIA_URL}

    return render(request, "backend/admin.html", content)

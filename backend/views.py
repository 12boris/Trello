from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import HttpResponseRedirect, render
from .models import Card, Action, Comment, Day, Idea
from authapp.models import BaseIdeinerUser
from django.contrib.auth.decorators import user_passes_test
import datetime
import os, shutil


def DateIsBigger(action_date):
    date = datetime.date.today().strftime('%d.%m.%Y')

    try:
        date_is_bigger = datetime.datetime.strptime(date, '%d.%m.%Y') >= datetime.datetime.strptime(action_date, '%d.%m.%Y')
    except:
        date_is_bigger = datetime.datetime.strptime(datetime.date.today().strftime('%d.%m.%y'), '%d.%m.%y') >= datetime.datetime.strptime(action_date, '%d.%m.%y')

    return date_is_bigger


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
        action = Action.objects.filter(card=card).order_by("progress")
        action_sl = {}
        aa = 0

        for act in action:
            date = datetime.date.today().strftime('%d.%m.%Y')
            date_is_bigger = DateIsBigger(act.date)

            aa += 1
            action_sl[aa] = {"action": act, "date_is_bigger": date_is_bigger}

        sl_ideas[a] = {"action": action_sl,"card": card}

    return sl_ideas


""" главное меню """


def main(request):
    title = "Карточки"

    card = GenIdeasList(Card.objects.all().order_by("-created_at"))
    date = datetime.date.today().strftime('%d.%m.%y')
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]

    content = {"title": title, "card": card, "date": date, "image": image}

    return render(request, "backend/index.html", content)


def calendar(request):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Календарь"
    days = Day.objects.all().order_by("pk")

    days_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    weeks, week = [], []
    a = 0

    for i in days:
        a += 1
        week.append({"day": i, "days_of_week": days_of_week[a - 1]})

        if a == 7:
            weeks.append(week)
            week = []
            a = 0

    print([i for i in weeks], '\n',  len(weeks))

    content = {"title": title, "weeks": weeks, "image": image   } 

    return render(request, "backend/calendar.html", content)


""" settings """


def settings(request):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Настройки"
    
    img = []

    for file in os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\img"):
        img.append(file)

    content = {"title": title, "img": img, "image": image}

    return render(request, "backend/settings.html", content)


def change_image(request, name):

    file = f"C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\img\\{name}"
    dir = "C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image"
    first_file = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")
    os.remove(f"C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image\\{first_file[0]}")
    shutil.copy(file, dir)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" дни """


def day_add(request):
    days = Day.objects.all()

    if days:
        last_day_date = days.last().date
        date = (last_day_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
    else:
        date = (datetime.date.today()).strftime('%Y-%m-%d')

    if len(days) % 7 == 0:
        day = Day.objects.create(date=date)
        day.save()

    else:
        day = Day.objects.create(date=date)
        day.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def day_edit(request):

    pk_list = [i.pk for i in Day.objects.all()]
    four_words_list = ['first', 'second', 'third', 'fourth']

    for pk in pk_list:
        for word in four_words_list:
            try:
                if request.POST[f'{word}-{pk}']:
                    day = Day.objects.filter(pk=pk).first()
                    if word == 'first': day.first_is_active = True
                    if word == 'second': day.second_is_active = True
                    if word == 'third': day.third_is_active = True
                    if word == 'fourth': day.fourth_is_active = True
                    day.save()
            except:
                pass

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" ideas """


def ideas(request):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Идеи"

    inactive_ideas = Idea.objects.filter(is_active=False)
    active_ideas = Idea.objects.filter(is_active=True)

    content = {"title": title, "image": image, "inactive_ideas": inactive_ideas, "active_ideas": active_ideas}

    return render(request, "backend/ideas.html", content)


def idea_add(request):

    name = request.POST['name']
    final_date = request.POST['date']
    describe = request.POST['describe']

    new_idea = Idea.objects.create(name=name ,final_date=final_date, describe=describe)
    new_idea.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def activate_idea(request, pk):

    idea = Idea.objects.filter(pk=pk).first()
    idea.is_active = True
    idea.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def idea_page(request, pk):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Страница идеи"

    idea = Idea.objects.filter(pk=pk).first()
    actions_list = idea.actions
    actions, days = [], []

    for pk in actions_list.split(" "):
        try:
            action = Action.objects.filter(pk=pk).first()
            actions.append(action)
            days.append(action.idea)
        except:
            print("hello")

    content = {"title": title, "image": image, "idea": idea, "actions": actions, "days": days}

    return render(request, "backend/idea_page.html", content)


def idea_delete(request, pk):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Идеи"

    idea = Idea.objects.filter(pk=pk)
    idea.delete()

    inactive_ideas = Idea.objects.filter(is_active=False)
    active_ideas = Idea.objects.filter(is_active=True)

    content = {"title": title, "image": image, "inactive_ideas": inactive_ideas, "active_ideas": active_ideas}

    return render(request, "backend/ideas.html", content)


def action_to_idea(request, pk):

    idea_name = request.POST["name"].strip()
    idea = Idea.objects.filter(name=idea_name).first()

    if str(pk) not in idea.actions:
        idea.actions = idea.actions + " " + str(pk)
    idea.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


""" карточки """


def card_add(request):

    author = request.user.username
    last_day = Card.objects.first().name
    name = last_day.split(" ")
    number = int(name[1]) + 1
    new_name = name[0] + " " + str(number)

    new_card = Card.objects.create(author=author, name=new_name)
    new_card.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def card_delete(request, pk):

    card = Card.objects.filter(pk=pk)
    card.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

""" действия """


def action_card(request, pk):
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Действие"
    action = Action.objects.filter(pk=pk).first()
    comments = Comment.objects.filter(action=action)
    date = datetime.date.today().strftime('%d.%m.%Y')
    idea_action = ""

    for idea in Idea.objects.all():
        if str(pk) in idea.actions.split(" "):
            idea_action = idea.name
    
    date_is_bigger = DateIsBigger(action.date)

    content = {"title": title, "action": action, "date": date, "comments": comments, "image": image, 
               "date_is_bigger": date_is_bigger, "idea_action": idea_action}

    return render(request, "backend/action_card.html", content)


def action_add(request):

    name_card = request.POST['name-card']
    card = Card.objects.filter(name=name_card).first()
    
    name = request.POST['name']
    date = request.POST['date']
    describe = request.POST['describe']
    importance = request.POST['importance']
    complexity = request.POST['complexity']
    author = request.user.username

    if str(date).lower() == "завтра":
        date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%y')

    if str(date).lower() == "сегодня":
        date = datetime.date.today().strftime('%d.%m.%y')

    new_action = Action.objects.create(name=name, author=author, date=date, describe=describe, card=card, 
                                       importance=importance, complexity=complexity)
    new_action.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def action_edit(request, pk):
    
    action = Action.objects.filter(pk=pk).first()
    
    try:
        if request.POST["progress"]: action.progress = request.POST["progress"]
    except:pass

    try:
        if request.POST["importance"]: action.importance = request.POST['importance']
        if request.POST["complexity"]: action.complexity = request.POST['complexity']
        if request.POST["name"]: action.name = request.POST["name"]

        if request.POST["date"]: 
            date = request.POST["date"]
            if str(date).lower() == "завтра":
                date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%y')

            if str(date).lower() == "сегодня":
                date = datetime.date.today().strftime('%d.%m.%y')
            action.date = date

        if request.POST["describe"]: action.describe = request.POST["describe"]
    except:pass

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

    if not comment:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

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
    image = os.listdir("C:\\Users\\пк\\Documents\\Projects\\Ich\\static\\use_image")[0]
    title = "Админка"
    
    card = Card.objects.all()

    content = {"title": title, "card": card, "image": image}

    return render(request, "backend/admin.html", content)

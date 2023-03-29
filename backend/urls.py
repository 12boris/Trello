from backend import views
from django.views.generic import RedirectView
from django.urls import path, include
import backend.views as backend


app_name = 'backend'

urlpatterns = [
    path("", backend.main, name="index"),
    path("admin/", backend.admin, name="admin"),
    path("main/", backend.main, name="main"),
    path("settings/", backend.settings, name="settings"),

    path("change_image/<str:name>/", backend.change_image, name="change_image"),

    path("calendar/", backend.calendar, name="calendar"),
    path("day_add/", backend.day_add, name="day_add"),
    path("day_edit/", backend.day_edit, name="day_edit"),

    path("ideas/", backend.ideas, name="ideas"),
    path("idea_add/", backend.idea_add, name="idea_add"),
    path("idea_delete/<int:pk>/", backend.idea_delete, name="idea_delete"),
    path("idea_page/<int:pk>/", backend.idea_page, name="idea_page"),
    path("activate_idea/<int:pk>/", backend.activate_idea, name="activate_idea"),
    path("action_to_idea/<int:pk>/", backend.action_to_idea, name="action_to_idea"),

    path("card_add/", backend.card_add, name="card_add"),
    path("card_delete/<int:pk>/", backend.card_delete, name="card_delete"),
    
    path("action_card/<int:pk>/", backend.action_card, name="action_card"),
    path("action_add/", backend.action_add, name="action_add"),
    path("action_delete/<int:pk>/", backend.action_delete, name="action_delete"),
    path("action_edit/<int:pk>/", backend.action_edit, name="action_edit"),
    
    path("comment_add/<int:pk>/", backend.comment_add, name="comment_add"),
    path("comment_delete/<int:pk>/", backend.comment_delete, name="comment_delete"),
]
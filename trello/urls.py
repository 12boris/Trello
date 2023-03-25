from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

app_name = 'config'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RedirectView.as_view(url="backend/")),
    path("backend/", include("backend.urls", namespace='backend')),
    path("authapp/", include("authapp.urls", namespace='authapp')),
]
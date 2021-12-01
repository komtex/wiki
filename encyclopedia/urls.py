from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("new", views.new, name="newpage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.randomPage, name="random")
]

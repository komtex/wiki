from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.EntryPage, name="entryPage"),
    path("new", views.new, name="newPage"),
    path("edit/<str:title>", views.edit, name="edit"),   
    path("random", views.randomPage, name="random")    
]

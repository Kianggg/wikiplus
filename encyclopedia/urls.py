from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.addpage, name="addpage"),
    path("edit", views.editpage, name="editpage"),
    path("random", views.randompage, name="randompage"),
    path("replace", views.replace, name="replace"),
    path("<str:pagename>", views.wikipage, name="wikipage")
]

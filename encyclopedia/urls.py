from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.take, name="take"),
    path("create", views.create, name="create"),
    path("random_page", views.random_page, name="random"),
    path("results", views.results, name="results"),
    path("edit", views.edit, name="edit"),
]

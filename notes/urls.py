from django.urls import path
from . import views

urlpatterns = [

    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_note, name="add_note"),
    path("my-notes/", views.my_notes, name="my_notes"),
    path("search/", views.search_page, name="search"),
    path("api/search/", views.search_api, name="search_api"),
    path("edit/<int:id>/", views.edit_note, name="edit_note"),
    path("delete/<int:id>/", views.delete_note, name="delete_note"),
    path(
    "api/suggest-category/",
    views.suggest_category_api,
    name="suggest_category"
),
path(
    "view/<int:id>/",
    views.view_note,
    name="view_note"
),
path("settings/", views.settings_page, name="settings"),
path(
    "summary/<int:id>/",
    views.summarize_note,
    name="summarize_note"
),
]
# projects/urls.py
from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("<slug:slug>/", views.project_detail, name="project_detail"),
    path("", views.project_list, name="project_list"),
    path("like/<int:pk>/", views.like_project, name="like_project"),
    path("comment/<int:pk>/", views.add_comment, name="add_comment"),
]
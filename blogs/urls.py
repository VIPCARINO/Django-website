# blogs/urls.py
from django.urls import path
from . import views
from . import api_views

app_name = "blogs"

urlpatterns = [
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("", views.blog_list, name="blog_list"),
    path("like/<int:pk>/", views.like_blog, name="like_blog"),
    path("comment/<int:pk>/", views.add_comment, name="add_comment"),
    path( "api/create-blog/", api_views.create_blog, name="create_blog" ),
]
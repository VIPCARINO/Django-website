from django.urls import path
from .views import home, about, search

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("search/", search, name="search"),
    
]
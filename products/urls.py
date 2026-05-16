from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("<slug:slug>/like/", views.toggle_like, name="toggle_like"),
    path("<slug:slug>/rate/", views.rate_product, name="rate_product"),

]
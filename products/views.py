from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, ProductCategory
from django.db.models import Avg

def product_list(request):

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")

    products = Product.objects.all().order_by("-created_at")

    # SEARCH
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tech_stack__icontains=query) |
            Q(category__name__icontains=query)
        )

    # FILTER BY CATEGORY
    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = ProductCategory.objects.all()

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "category_slug": category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    avg_rating = product.ratings.aggregate(avg=Avg("rating"))["avg"]
    context = {
        "product": product,
        "avg_rating": avg_rating,
    }

    return render(request, "products/product_detail.html", context)

from django.contrib.auth.decorators import login_required
from .models import Product, ProductLike


@login_required
def toggle_like(request, slug):
    product = get_object_or_404(Product, slug=slug)

    like, created = ProductLike.objects.get_or_create(
        product=product,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect("products:product_detail", slug=slug)

from .models import ProductRating

@login_required
def rate_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        value = int(request.POST.get("rating"))

        ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={"rating": value}
        )

    return redirect("products:product_detail", slug=slug)
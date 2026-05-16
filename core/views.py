from django.core.paginator import Paginator
from django.shortcuts import render

from projects.models import Project, ProjectCategory
from blogs.models import Blog, BlogCategory
from products.models import Product, ProductCategory
from .models import AboutPage, Skill, Journey
from products.models import Product
from django.db.models import Q


def home(request):

    project_list = Project.objects.order_by("-created_at")

    paginator = Paginator(project_list, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    latest_projects = Project.objects.order_by("-created_at")[:2]
    blogs = Blog.objects.order_by()[:2]
    latest_blogs = Blog.objects.order_by("-created_at")[:4]
    featured_products = Product.objects.filter(featured=True)[:3]

    project_categories = ProjectCategory.objects.all()
    blog_categories = BlogCategory.objects.all()
    product_categories = ProductCategory.objects.all()

    context = {
        "page_obj": page_obj,
        "latest_projects": latest_projects,
        "latest_blogs": latest_blogs,
        "blogs": blogs,
        "featured_products": featured_products,
        "project_categories": project_categories,
        "blog_categories": blog_categories,
        "product_categories": product_categories,
    }

    # 👇 THIS IS KEY (HTMX partial request)
    if request.headers.get("HX-Request"):
        return render(request, "core/partials/projects.html", context)

    return render(request, "core/home.html", context)

def about(request):

    about = AboutPage.objects.first()

    skills = Skill.objects.all()

    journeys = Journey.objects.all()

    featured_projects = Project.objects.filter(
        featured=True
    )[:6]

    latest_projects = Project.objects.order_by(
        "-created_at"
    )[:4]

    context = {
        "about": about,
        "skills": skills,
        "journeys": journeys,
        "featured_projects": featured_projects,
        "latest_projects": latest_projects,
    }

    return render(request, "core/about.html", context)

from django.db.models import Q
from projects.models import Project
from blogs.models import Blog
from products.models import Product

def search(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return render(request, "core/search.html", {
            "query": query,
            "projects": [],
            "blogs": [],
            "products": [],
        })

    # PROJECT SEARCH
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    )

    # BLOG SEARCH
    blogs = Blog.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    )

    # PRODUCT SEARCH (FIXED)
    products = Product.objects.filter(
        Q(title__icontains=query) |
    Q(description__icontains=query) |
    Q(tech_stack__icontains=query) |
    Q(category__name__icontains=query)
    )

    return render(request, "core/search.html", {
        "query": query,
        "projects": projects,
        "blogs": blogs,
        "products": products,
    })
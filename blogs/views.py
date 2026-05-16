# blogs/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Blog, BlogComment, BlogLike
from django.contrib.auth.decorators import login_required
from projects.models import Project

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    blog_categories = Blog.objects.values_list("category__name", flat=True).distinct()
    project_categories = Project.objects.values_list("category__name", flat=True).distinct()

    context = {
        "blog": blog,
        "blog_categories": blog_categories,
        "project_categories": project_categories,
    }
    return render(request, "blogs/detail.html", context)

def blog_list(request):
    category = request.GET.get("category")

    if category and category != "all":
        blogs = Blog.objects.filter(category__name=category)
    else:
        blogs = Blog.objects.all()

    blog_categories = Blog.objects.values_list("category__name", flat=True).distinct()
    project_categories = Project.objects.values_list("category__name", flat=True).distinct()

    context = {
        "blogs": blogs,
        "blog_categories": blog_categories,
        "project_categories": project_categories,
        "active_category": category or "all"
    }

    # 👇 THIS IS THE FIX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "blogs/blog_list.html", context)

    return render(request, "blogs/blog_list.html", context)

@login_required
def like_blog(request, pk):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "login required"}, status=403)
    
    blog =Blog.objects.get(pk=pk)
    user = request.user

    like, created = BlogLike.objects.get_or_create(
        blog=blog,
        user=user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes": blog.likes.count()
    })

@login_required
def add_comment(request, pk):

    if request.method == "POST":

        blog = Blog.objects.get(pk=pk)

        comment = BlogComment.objects.create(
            blog=blog,
            user=request.user,
            body=request.POST.get("body")
        )

        return JsonResponse({
            "name": request.user.username,
            "email": request.user.email,
            "body": comment.body
        })

    return JsonResponse({"error": "Invalid request"})
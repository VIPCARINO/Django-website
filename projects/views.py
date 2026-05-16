# projects/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, ProjectComment, ProjectLike, ProjectCode
from django.contrib.auth.decorators import login_required
from blogs.models import Blog
from urllib.parse import urlparse, parse_qs


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project_categories = Project.objects.values_list("category__name", flat=True).distinct()
    blog_categories = Blog.objects.values_list("category__name", flat=True).distinct()
    code = ProjectCode.objects.all()

    context = {
        "project": project,
        "project_categories": project_categories,
        "blog_categories": blog_categories,
        "code": code
    }
    return render(request, "projects/detail.html", context)

def project_list(request):
    category = request.GET.get("category")

    if category and category != "all":
        projects = Project.objects.filter(category__name=category)
    else:
        projects = Project.objects.all()

    project_categories = Project.objects.values_list("category__name", flat=True).distinct()
    blog_categories = Blog.objects.values_list("category__name", flat=True).distinct()

    context = {
        "projects": projects,
        "project_categories": project_categories,
        "blog_categories": blog_categories,
        "active_category": category or "all"
    }

    # 👇 THIS IS THE FIX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "projects/project_list.html", context)

    return render(request, "projects/project_list.html", context)

@login_required
def like_project(request, pk):

    if not request.user.is_authenticated:
        return JsonResponse({"error": "login required"}, status=403)
    
    project = Project.objects.get(pk=pk)
    user = request.user

    like, created = ProjectLike.objects.get_or_create(
        project=project,
        user=user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes": project.likes.count()
    })

@login_required
def add_comment(request, pk):

    if request.method == "POST":

        project = Project.objects.get(pk=pk)

        comment = ProjectComment.objects.create(
            project=project,
            user=request.user,
            body=request.POST.get("body")
        )

        return JsonResponse({
            "name": request.user.username,
            "email": request.user.email,
            "body": comment.body
        })

    return JsonResponse({"error": "Invalid request"})

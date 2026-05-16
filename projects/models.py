from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )

    github_url = models.URLField(blank=True)

    live_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    youtube_url = models.URLField(blank=True, null=True)

    video = models.URLField(blank=True, null=True)

    def get_absolute_url(self):

        return reverse(
            "projects:project_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):
        return self.title
    

class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.project.title}"
    
class ProjectLike(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "user")

class ProjectCode(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="snippets"
    )

    title = models.CharField(max_length=100)

    language = models.CharField(max_length=50)

    code = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.project.title}"